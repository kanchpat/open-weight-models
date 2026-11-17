"""Builds docs/index.html, the interactive course site, as one self-contained file.

Sources: site/src/ (course.js lesson data, app.js, style.css, index.tpl.html) and the
primary-source list from whitepaper/enterprise-playbook.md. Standard library only.
"""
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "site", "src")
WP = os.path.join(REPO, "whitepaper", "enterprise-playbook.md")
OUT = os.path.join(REPO, "docs", "index.html")


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()


def sources():
    """Returns the numbered primary sources from the playbook bibliography."""
    out = []
    with open(WP, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"- (\*\*\[\d+\]\*\* .*)", line.strip())
            if m:
                out.append(m.group(1))
    if not out:
        raise SystemExit("No primary sources found in " + WP)
    return out


def main():
    js = "const SOURCES = " + json.dumps(sources(), ensure_ascii=False) + ";\n" + read("course.js") + "\n" + read("app.js")
    if "</script" in js.lower():
        raise SystemExit("site/src JavaScript must not contain a closing script tag")
    html = read("index.tpl.html").replace("/*CSS*/", read("style.css")).replace("/*JS*/", js)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("Built interactive course site at:", OUT, "Size:", len(html.encode("utf-8")))


if __name__ == "__main__":
    main()
