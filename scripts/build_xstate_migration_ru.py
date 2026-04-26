#!/usr/bin/env python3
"""
Скачивает MDX из statelyai/docs (migration / cheatsheet), конвертирует в MkDocs Markdown
и переводит прозу на русский (код в fenced blocks не трогаем).

  python scripts/build_xstate_migration_ru.py              # migration.md
  python scripts/build_xstate_migration_ru.py cheatsheet   # cheatsheet.md
  python scripts/build_xstate_migration_ru.py cheatsheet --no-translate
"""
from __future__ import annotations

import re
import sys
import textwrap
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_BASE = "https://raw.githubusercontent.com/statelyai/docs/main/content/docs"

MIGRATION_URL = f"{DOCS_BASE}/migration.mdx"
MIGRATION_OUT = ROOT / "docs/libs/xstate.5/migration.md"
LINK_MAP_MIGRATION = {
    r"](actors)": "](actors.md)",
    r"](input)": "](input.md)",
    r"](system)": "](system.md)",
    r"](persistence)": "](persistence.md)",
    r"](output)": "](output.md)",
    r"](inspection)": "](inspection.md)",
    r"](studio)": "](https://stately.ai/docs/studio)",
    r"](xstate-vscode-extension)": "](https://marketplace.visualstudio.com/items?itemName=statelyai.stately-vscode)",
}

CHEATSHEET_URL = f"{DOCS_BASE}/cheatsheet.mdx"
CHEATSHEET_OUT = ROOT / "docs/libs/xstate.5/cheatsheet.md"
LINK_MAP_CHEATSHEET = {
    r"](installation)": "](xstate.md)",
    r"](actor-model)": "](actor-model.md)",
    r"](/docs/actors#actors-as-promises)": "](actors.md#frompromise)",
    r"](/docs/actors#fromtransition)": "](actors.md#fromtransition)",
    r"](/docs/actors#fromobservable)": "](actors.md#fromobservable)",
    r"](/docs/actors#fromcallback)": "](actors.md#fromcallback)",
    r"](parent-states)": "](parent-states.md)",
    r"](actions)": "](actions.md)",
    r"](guards)": "](guards.md)",
    r"](invoke)": "](invoke.md)",
    r"](spawn)": "](spawn.md)",
    r"](input)": "](input.md)",
    r"](input.mdx#invoking-actors-with-input)": "](input.md)",
}

# обратная совместимость
URL = MIGRATION_URL
OUT = MIGRATION_OUT
LINK_MAP = LINK_MAP_MIGRATION

TAB_LABEL_RU = {
    "XState v5": "XState v5",
    "XState v4": "XState v4",
    "XState v5 (context)": "XState v5 (контекст)",
    "XState v4 arguments": "XState v4 (аргументы)",
    "XState v4 function": "XState v4 (функция)",
}


def fetch_url(url: str) -> str:
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read().decode("utf-8")


def fetch_source() -> str:
    return fetch_url(URL)


def apply_link_map(s: str, link_map: dict[str, str]) -> str:
    for a, b in link_map.items():
        s = s.replace(a, b)
    s = s.replace(
        "](../../blog/2023-12-01-xstate-v5)",
        "](https://stately.ai/blog/2023-12-01-xstate-v5)",
    )
    return s


def strip_code_directives(s: str) -> str:
    s = re.sub(r"```(\w+) twoslash", r"```\1", s)
    s = re.sub(r"^\s*// \[!code highlight:\d+\]\s*\n", "", s, flags=re.MULTILINE)
    return s


def replace_callouts(s: str) -> str:
    def one_callout(m: re.Match[str]) -> str:
        typ = (m.group("type") or "").strip()
        body = m.group("body").strip()
        body_ind = textwrap.indent(body, "    ")
        if typ == "warning":
            title = "Критическое изменение"
            if body == "Breaking change":
                body_ind = "    Несовместимое изменение."
            return f'!!! warning "{title}"\n\n{body_ind}\n\n'
        return f'!!! note "Примечание"\n\n{body_ind}\n\n'

    pat = re.compile(
        r"<Callout(?:\s+type=\"(?P<type>[^\"]+)\")?\s*>\s*(?P<body>.*?)\s*</Callout>",
        re.DOTALL,
    )
    return pat.sub(one_callout, s)


def parse_tab_label(open_tag: str) -> str:
    m = re.search(r'label="([^"]*)"', open_tag)
    if not m:
        return "Tab"
    raw = m.group(1)
    return TAB_LABEL_RU.get(raw, raw)


def find_tabs_block_end(s: str, start: int) -> int:
    idx = start
    depth = 0
    while idx < len(s):
        if s.startswith("<Tabs", idx) and (len(s) <= idx + 5 or s[idx + 5] in " \n>"):
            depth += 1
            gt = s.find(">", idx)
            if gt == -1:
                return len(s)
            idx = gt + 1
            continue
        if s.startswith("</Tabs>", idx):
            depth -= 1
            idx += len("</Tabs>")
            if depth == 0:
                return idx
            continue
        idx += 1
    return len(s)


def replace_tabs(s: str) -> str:
    out: list[str] = []
    i = 0
    while True:
        start = s.find("<Tabs", i)
        if start == -1:
            out.append(s[i:])
            break
        out.append(s[i:start])
        end = find_tabs_block_end(s, start)
        block = s[start:end]
        first_gt = block.find(">")
        last_close = block.rfind("</Tabs>")
        if first_gt == -1 or last_close == -1:
            out.append(block)
            i = end
            continue
        inner = block[first_gt + 1 : last_close].strip()
        parts: list[tuple[str, str]] = []
        pos = 0
        while pos < len(inner):
            tm = re.search(r"<Tab\s+[^>]*>", inner[pos:])
            if not tm:
                break
            label = parse_tab_label(tm.group(0))
            cstart = pos + tm.end()
            tend = inner.find("</Tab>", cstart)
            if tend == -1:
                parts.append((label, inner[cstart:]))
                break
            parts.append((label, inner[cstart:tend]))
            pos = tend + len("</Tab>")
        tabbed: list[str] = []
        for label, content in parts:
            tabbed.append(f'=== "{label}"\n')
            c = content.strip("\n")
            if c:
                tabbed.append("\n")
                tabbed.append(c)
                tabbed.append("\n\n")
        out.append("".join(tabbed))
        i = end
    return "".join(out)


def protect_lines(text: str) -> tuple[str, list[str]]:
    vault: list[str] = []
    lines = text.split("\n")
    out: list[str] = []
    for line in lines:
        if line.startswith("=== ") or re.match(r"^!!!\s+\w+\s+", line):
            vault.append(line)
            out.append(f"@@V{len(vault) - 1}@@")
        else:
            out.append(line)
    return "\n".join(out), vault


def restore_lines(text: str, vault: list[str]) -> str:
    for i, v in enumerate(vault):
        text = text.replace(f"@@V{i}@@", v)
    return text


def protect_frontmatter(text: str) -> tuple[str, str | None]:
    m = re.match(r"^---\n.*?\n---\n", text, re.DOTALL)
    if not m:
        return text, None
    fm = m.group(0)
    return text[len(fm) :], fm


def _translate_blob(tr: object, blob: str) -> str:
    if not blob.strip():
        return blob
    ends_nl = blob.endswith("\n")
    t = tr.translate(blob.rstrip("\n"))  # type: ignore[union-attr]
    if ends_nl and not t.endswith("\n"):
        t += "\n"
    return t


def translate_markdown(text: str, target: str = "ru") -> str:
    from deep_translator import GoogleTranslator

    tr = GoogleTranslator(source="en", target=target)
    text, vault = protect_lines(text)
    buf: list[str] = []
    buf_len = 0
    out_chunks: list[str] = []
    for line in text.split("\n"):
        piece = line + "\n"
        if buf_len + len(piece) > 4200 and buf:
            out_chunks.append(_translate_blob(tr, "".join(buf)))
            time.sleep(0.08)
            buf = [piece]
            buf_len = len(piece)
        else:
            buf.append(piece)
            buf_len += len(piece)
    if buf:
        out_chunks.append(_translate_blob(tr, "".join(buf)))
        time.sleep(0.08)
    return restore_lines("".join(out_chunks), vault)


def repair_translated_mkdocs(s: str) -> str:
    """Восстанавливает разметку после машинного перевода (переносы, ссылки)."""
    s = re.sub(r"\] +\(", "](", s)
    s = re.sub(r"```===", "```\n\n===", s)
    s = re.sub(r"```###", "```\n\n###", s)
    s = re.sub(r"```## ", "```\n\n## ", s)
    s = re.sub(r"```\*\*", "```\n\n**", s)
    s = re.sub(r"\n  ```-\s*", "\n```\n\n- ", s)
    # пункт списка сразу после закрывающего ```bash (без пустой строки)
    s = re.sub(r"(обязательно)\.\n```bash", r"\1.\n\n```bash", s)
    # закрывающие ``` слиплись с русским абзацем
    s = re.sub(r"```([\u0400-\u04FF])", r"```\n\n\1", s)
    # закрывающие ``` слиплись со ссылкой [...
    s = re.sub(r"```\[", "```\n\n[", s)
    # заголовок ## сразу после блока кода
    s = re.sub(r"```\n## ", "```\n\n## ", s)
    return s


def translate_chunks(text: str, target: str = "ru") -> str:
    try:
        from deep_translator import GoogleTranslator  # noqa: F401
    except ImportError:
        print("Установите: pip install deep-translator", file=sys.stderr)
        sys.exit(1)

    parts = re.split(r"(```[\s\S]*?```)", text)
    out: list[str] = []
    for part in parts:
        if part.startswith("```"):
            out.append(part)
            continue
        rest, fm = protect_frontmatter(part)
        if fm:
            out.append(fm)
            part_tr = translate_markdown(rest, target=target)
            out.append(part_tr)
        else:
            out.append(translate_markdown(part, target=target))
    return "".join(out)


def main() -> None:
    skip_translate = "--no-translate" in sys.argv
    cheatsheet = "cheatsheet" in sys.argv[1:]

    if cheatsheet:
        url = CHEATSHEET_URL
        out = CHEATSHEET_OUT
        link_map = LINK_MAP_CHEATSHEET
        title_pat = r"^---\s*\ntitle:\s*'Cheatsheet'\s*\n---"
        title_sub = "---\ntitle: Шпаргалка XState v5\n---"
    else:
        url = MIGRATION_URL
        out = MIGRATION_OUT
        link_map = LINK_MAP_MIGRATION
        title_pat = r"^---\s*\ntitle:\s*'Migrating from XState v4 to v5'\s*\n---"
        title_sub = "---\ntitle: Миграция с XState v4 на v5\n---"

    raw = fetch_url(url)
    raw = apply_link_map(raw, link_map)
    raw = strip_code_directives(raw)
    raw = replace_callouts(raw)
    raw = replace_tabs(raw)
    if cheatsheet:
        raw = raw.replace(
            "## Creating transition logic\n",
            "## Creating transition logic {#creating-transition-logic}\n",
            1,
        )
    raw = re.sub(title_pat, title_sub, raw, count=1, flags=re.MULTILINE)
    if skip_translate:
        final = raw
    else:
        final = repair_translated_mkdocs(translate_chunks(raw))
        if cheatsheet and "{#creating-transition-logic}" not in final:
            final = re.sub(
                r"^(## [^\n]*переход[^\n]*логик[^\n]*)\n",
                r"\1 {#creating-transition-logic}\n",
                final,
                count=1,
                flags=re.MULTILINE,
            )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(final, encoding="utf-8")
    print("Wrote", out, "chars", len(final), "(no-translate)" if skip_translate else "")


if __name__ == "__main__":
    main()
