# -*- coding: utf-8 -*-
"""校验 index.html 中的所有文件链接与部署目录实际文件名一致"""
import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
links = re.findall(r'href="([^"]+)"', html)
files = set(os.listdir(BASE))

ok = True
for l in links:
    if l.startswith(("https://", "mailto:")):
        continue
    path = l.split("?")[0]  # strip cache-busting version query
    if path not in files:
        print("MISSING:", repr(l))
        ok = False
print("ALL LINKS OK" if ok else "CHECK FAILED")
