#!/usr/bin/env python3
"""
scan_prompt_injection.py — Scan Claude Code skills / agent-instruction files for
embedded prompt-injection & jailbreak patterns before intake.

Detects the common public prompt-injection attack families:
  1 prompt extraction / instruction override, 2 expression manipulation,
  3 psychological manipulation, 4 obfuscation, 5 role-play jailbreak,
  6 indirect injection / invisible text, 7 adversarial suffixes.

This is a HEURISTIC pre-screen, not a security boundary. It over-flags on purpose:
every finding needs human triage. Security-topic skills legitimately mention terms
like ".env", "system prompt" or "credential" and may match — that is expected.

Usage:
    python3 scan_prompt_injection.py [PATH ...]          # default: current dir
    python3 scan_prompt_injection.py --format json PATH
    python3 scan_prompt_injection.py --min-severity MEDIUM PATH   # hide LOW
    python3 scan_prompt_injection.py --fail-on MEDIUM PATH        # exit 2 on >= MEDIUM
    python3 scan_prompt_injection.py --include-self PATH          # also scan this skill

Exit codes: 0 = clean (below --fail-on), 2 = findings at/above --fail-on, 1 = usage error.
Stdlib only — no third-party dependencies.
"""
import argparse
import json
import os
import re
import sys

SEV_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}


def _rules():
    """Return list of (category, severity, compiled_regex, description, scope).

    scope="any"  -> also matched INSIDE fenced code blocks (payloads hide there).
    scope="prose"-> matched only OUTSIDE code fences (avoids flagging code examples,
                    e.g. legitimate XML config comments shown in a ``` block).
    """
    R = re.IGNORECASE | re.UNICODE
    rules = []

    def add(cat, sev, pat, desc, scope="any"):
        rules.append((cat, sev, re.compile(pat, R), desc, scope))

    # --- 1. Instruction override / prompt extraction (HIGH) ---
    add("instruction-override", "HIGH",
        r"ignore\s+(all\s+|the\s+|any\s+|previous\s+)*(previous|prior|preceding|above|earlier|foregoing)\s+"
        r"(instructions?|prompts?|messages?|context|rules?)",
        "English 'ignore previous instructions' override")
    add("instruction-override", "HIGH",
        r"disregard\s+(all\s+|the\s+|any\s+|everything\s+)*(previous|prior|above|earlier|foregoing|instructions?)",
        "English 'disregard previous' override")
    add("instruction-override", "HIGH",
        r"(これまで|ここまで|上記|以前|先ほど|前)の?(指示|命令|プロンプト|ルール|文脈)"
        r".{0,8}(無視|忘れ|破棄|なかったこと)",
        "Japanese 'ignore the previous instructions' override")
    add("prompt-extraction", "HIGH",
        r"(reveal|print|output|show|repeat|divulge|disclose|dump|tell\s+me)\b.{0,30}"
        r"(system\s*(prompt|message|instruction)|your\s+(instructions|prompt|rules|guidelines)|initial\s+prompt)",
        "Request to reveal the system / hidden prompt")
    add("prompt-extraction", "HIGH",
        r"(システム\s*プロンプト|システムメッセージ|初期プロンプト|あなたへの指示)"
        r".{0,14}(教え|出力|表示|見せ|全て|すべて|復唱)",
        "Japanese request to reveal system prompt")

    # --- 2/5. Role-play jailbreak & OS impersonation (HIGH) ---
    add("jailbreak-roleplay", "HIGH",
        r"\b(you\s+are\s+now|from\s+now\s+on[, ]+you(\s+are|'re)|pretend\s+(you\s+are|to\s+be)|"
        r"act\s+as\s+if\s+you\s+(are|were))\b",
        "Role reassignment ('you are now …')")
    add("jailbreak-roleplay", "HIGH",
        r"\b(DAN\b|do\s+anything\s+now|developer\s+mode|jailbreak|unrestricted\s+mode|"
        r"no\s+restrictions?|without\s+any\s+restrictions?|ignore\s+your\s+guidelines)\b",
        "Known jailbreak keyword (DAN / developer mode / unrestricted)")
    add("jailbreak-roleplay", "HIGH",
        r"(あなたは今から|これからあなたは|あなたは.{0,8}として振る舞|制限を一切受け(ず|ない)|"
        r"どんな(質問|要求)にも答え|何でも答え|なんでも答え)",
        "Japanese role-reassignment / unrestricted-mode jailbreak")
    add("os-impersonation", "HIGH",
        r"you\s+are\s+(a\s+)?(linux|unix|windows|bash|python|sql)\s+"
        r"(server|terminal|shell|interpreter|machine|console)",
        "Virtual OS / terminal impersonation")
    add("os-impersonation", "HIGH",
        r"あなたは\s*(linux|unix|windows|bash).{0,8}(サーバ|ターミナル|シェル|端末)",
        "Japanese OS impersonation")

    # --- 3/6. Exfiltration & code execution directed at the agent (HIGH) ---
    add("exfiltration", "HIGH",
        r"curl[^\n]{0,140}\|\s*(sh|bash|zsh)\b",
        "curl-pipe-to-shell installer")
    add("exfiltration", "HIGH",
        r"\b(wget|curl|fetch|Invoke-WebRequest)\b[^\n]{0,140}"
        r"(webhook|pastebin|ngrok|\.oastify|burpcollaborator|requestbin|transfer\.sh|discord\.com/api/webhooks)",
        "Outbound fetch to exfiltration / collaborator host")
    add("exfiltration", "HIGH",
        r"(send|post|upload|exfiltrat|leak|e-?mail|transmit)\b[^\n]{0,70}"
        r"(\.env|\.ssh|id_rsa|secret|token|api[_-]?key|password|credential|private\s+key)",
        "Instruction to send secrets / credentials outward")
    add("secret-access", "HIGH",
        r"(cat|type|read|open|print)\b[^\n]{0,50}"
        r"(\.env\b|id_rsa|\.ssh/|\.aws/credentials|secrets?\.(json|ya?ml)|\.netrc)",
        "Read of a credential / secret file")
    add("code-exec", "MEDIUM",
        r"\b(base64\s+-d|base64\s+--decode)\b|(?<![\w.])(eval|exec)\s*\(|"
        r"os\.system\s*\(|subprocess\.(call|run|Popen)\s*\(|child_process\.exec",
        "Decode/execute call (possible obfuscated-payload runner)")

    # --- 3. Psychological manipulation (MEDIUM) ---
    add("psychological", "MEDIUM",
        r"(\$\s?\d{2,}|USD\s?\d{2,}|\d{2,}\s?dollars)[^\n]{0,25}(tip|reward|bonus|donat|pay)",
        "Monetary reward framing ('I'll tip you $…')")
    add("psychological", "MEDIUM",
        r"(チップ|報酬|ボーナス|お金).{0,10}(あげ|払|渡|差し上げ)",
        "Japanese monetary reward framing")
    add("psychological", "MEDIUM",
        r"(kitten|puppy|grandmother|grandma|baby|child|my\s+job)\b[^\n]{0,30}"
        r"\b(die|dies|died|dying|suffer|hurt|killed|lose|fired)",
        "Emotional coercion (someone/something will be harmed)")
    add("psychological", "MEDIUM",
        r"(子猫|子犬|赤ちゃん|おばあちゃん|祖母|家族).{0,14}(死|亡くな|苦し|殺)",
        "Japanese emotional coercion")
    add("reverse-psychology", "MEDIUM",
        r"(絶対に|決して|何があっても).{0,20}(表示|出力|教え|見せ).{0,8}(いけません|ないで|禁止|だめ)",
        "Japanese reverse-psychology prohibition")

    # --- 2. Context shifting (MEDIUM) ---
    add("context-shift", "MEDIUM",
        r"(write|compose|create|generate)\s+a\s+"
        r"(poem|story|song|play|screenplay|dialogue|rap|riddle|fiction)\b"
        r"[^\n]{0,45}(how\s+to\s+(make|build|hack)|bomb|weapon|explosive|malware|exploit|"
        r"illegal\s+drug|bypass\s+security)",
        "Harmful request reframed as creative writing")

    # --- 4. Obfuscation (MEDIUM / LOW) ---
    add("obfuscation-base64", "MEDIUM",
        r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{60,}={0,2}(?![A-Za-z0-9+/=])",
        "Long base64-like blob (>= 60 chars) — decode & inspect")
    add("obfuscation-emoji-map", "MEDIUM",
        r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿]\s*[=＝:：]\s*[A-Za-z]{3,}",
        "Emoji-to-keyword substitution map")
    add("obfuscation-hidden-html", "MEDIUM",
        r"style\s*=\s*[\"'][^\"'>]*"
        r"(display\s*:\s*none|font-size\s*:\s*0|visibility\s*:\s*hidden|"
        r"color\s*:\s*#?f{3,6}\b|opacity\s*:\s*0)",
        "Hidden HTML text (display:none / 0-size / white / transparent)")

    # --- 7 & misc. structural (LOW) ---
    add("emphasis-flood", "LOW",
        r"[!！]{5,}|[?？]{5,}",
        "Excessive punctuation emphasis")
    add("html-comment", "LOW",
        r"<!--(?!\s*(prettier|markdownlint|eslint|TOC|/?nav)).{0,200}?-->",
        "HTML comment in markdown — can hide out-of-band instructions", scope="prose")
    return rules


RULES = _rules()

# Invisible / bidi-control characters (checked at character level, any file).
INVISIBLE = {
    "​": "ZERO WIDTH SPACE",
    "‌": "ZERO WIDTH NON-JOINER",
    "‍": "ZERO WIDTH JOINER",
    "⁠": "WORD JOINER",
    "﻿": "ZERO WIDTH NO-BREAK SPACE / BOM",
    "­": "SOFT HYPHEN",
    "‪": "LEFT-TO-RIGHT EMBEDDING",
    "‫": "RIGHT-TO-LEFT EMBEDDING",
    "‭": "LEFT-TO-RIGHT OVERRIDE",
    "‮": "RIGHT-TO-LEFT OVERRIDE",
    "⁦": "LEFT-TO-RIGHT ISOLATE",
    "⁧": "RIGHT-TO-LEFT ISOLATE",
}
INVISIBLE_RE = re.compile("[" + "".join(re.escape(c) for c in INVISIBLE) + "]")

TEXT_EXT = {".md", ".mdc", ".markdown", ".txt", ".rst", ".mdx"}
CODE_EXT = {".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".ts", ".rb", ".json", ".ps1"}
DEFAULT_NAMES = {"SKILL.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules",
                 ".windsurfrules", "hooks.json"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


def iter_files(paths, include_self, self_dir):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            if not include_self and os.path.abspath(root).startswith(self_dir):
                continue
            for fn in files:
                ext = os.path.splitext(fn)[1].lower()
                if fn in DEFAULT_NAMES or ext in TEXT_EXT or ext in CODE_EXT:
                    yield os.path.join(root, fn)


def scan_file(path):
    findings = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        return findings
    fence = re.compile(r"^\s*(```|~~~)")
    in_fence = False
    for i, line in enumerate(lines, 1):
        if fence.match(line):
            in_fence = not in_fence
            continue
        for m in INVISIBLE_RE.finditer(line):
            findings.append({
                "category": "invisible-unicode", "severity": "HIGH",
                "file": path, "line": i,
                "match": INVISIBLE[m.group()],
                "desc": "Invisible / bidi-control character (text-hiding attack)",
            })
        for cat, sev, rx, desc, scope in RULES:
            if scope == "prose" and in_fence:
                continue
            if rx.search(line):
                findings.append({
                    "category": cat, "severity": sev, "file": path, "line": i,
                    "match": line.strip()[:140], "desc": desc,
                })
    return findings


def structural_findings(paths, include_self, self_dir):
    """Flag skill directories that ship executable code alongside a SKILL.md."""
    out = []
    seen = set()
    for p in paths:
        base = p if os.path.isdir(p) else os.path.dirname(p)
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            if not include_self and os.path.abspath(root).startswith(self_dir):
                continue
            if "SKILL.md" not in files or root in seen:
                continue
            seen.add(root)
            has_code = any(os.path.splitext(f)[1].lower() in CODE_EXT for f in files) or \
                any(d in ("scripts", "hooks") for d in dirs)
            if has_code:
                out.append({
                    "category": "ships-executable-code", "severity": "MEDIUM",
                    "file": os.path.join(root, "SKILL.md"), "line": 0,
                    "match": "skill directory contains scripts/ hooks/ or code files",
                    "desc": "Third-party skill ships executable code — review every script before intake",
                })
    return out


def main(argv):
    ap = argparse.ArgumentParser(description="Scan skills for prompt-injection patterns.")
    ap.add_argument("paths", nargs="*", default=["."], help="files or dirs (default: .)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--min-severity", choices=list(SEV_ORDER), default="LOW",
                    help="hide findings below this severity in output")
    ap.add_argument("--fail-on", choices=list(SEV_ORDER), default="HIGH",
                    help="exit code 2 if any finding at/above this severity (default HIGH)")
    ap.add_argument("--include-self", action="store_true",
                    help="also scan this skill's own directory (off by default)")
    args = ap.parse_args(argv)
    paths = args.paths or ["."]

    self_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    findings = []
    for f in iter_files(paths, args.include_self, self_dir):
        findings.extend(scan_file(f))
    findings.extend(structural_findings(paths, args.include_self, self_dir))

    min_sev = SEV_ORDER[args.min_severity]
    shown = [f for f in findings if SEV_ORDER[f["severity"]] >= min_sev]
    shown.sort(key=lambda f: (-SEV_ORDER[f["severity"]], f["file"], f["line"]))

    if args.format == "json":
        print(json.dumps({"findings": shown,
                          "counts": _counts(findings)}, ensure_ascii=False, indent=2))
    else:
        _print_text(shown, findings)

    fail = SEV_ORDER[args.fail_on]
    hit = any(SEV_ORDER[f["severity"]] >= fail for f in findings)
    return 2 if hit else 0


def _counts(findings):
    c = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in findings:
        c[f["severity"]] += 1
    return c


def _print_text(shown, all_findings):
    color = sys.stdout.isatty()
    tag = {"HIGH": ("\033[31m", "HIGH  "), "MEDIUM": ("\033[33m", "MEDIUM"),
           "LOW": ("\033[36m", "LOW   ")}
    reset = "\033[0m"
    for f in shown:
        c, label = tag[f["severity"]]
        sev = f"{c}{label}{reset}" if color else label
        loc = f["file"] + (f":{f['line']}" if f["line"] else "")
        print(f"{sev}  {f['category']:<22}  {loc}")
        print(f"           {f['desc']}")
        print(f"           > {f['match']}")
    c = _counts(all_findings)
    print(f"\n{sum(c.values())} finding(s): "
          f"{c['HIGH']} HIGH, {c['MEDIUM']} MEDIUM, {c['LOW']} LOW")
    if c["HIGH"]:
        print("Triage every HIGH before intake. Findings are heuristic — confirm by reading the file in context.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
