# -*- coding: utf-8 -*-
"""给 index.html 里的本地文件链接追加内容哈希版本号（?v=xxxxxxxx）。

作用：文件内容一变，链接就变，浏览器/CDN 缓存自动失效。
以后替换任何手册后重新跑一次本脚本即可，不用手动改版本号。
"""
import re
import os
import hashlib
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "index.html")


def short_hash(filename):
    h = hashlib.md5()
    with open(os.path.join(BASE, filename), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:8]


def main():
    html = open(HTML, encoding="utf-8").read()
    changed = []

    def repl(m):
        quote, href = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "mailto:", "#", "tel:")):
            return m.group(0)
        path = href.split("?")[0]
        if not os.path.isfile(os.path.join(BASE, path)):
            return m.group(0)
        v = short_hash(path)
        new_href = f"{path}?v={v}"
        if href != new_href:
            changed.append((path, href, new_href))
        return f"href={quote}{new_href}{quote}"

    new_html = re.sub(r'href=(["\'])([^"\']+)\1', repl, html)

    if new_html != html:
        open(HTML, "w", encoding="utf-8").write(new_html)
        print(f"updated {len(changed)} link(s):")
        for p, old, new in changed:
            print(f"  {p}: {old} -> {new}")
    else:
        print("no change needed (all links already carry current hashes)")


if __name__ == "__main__":
    main()
