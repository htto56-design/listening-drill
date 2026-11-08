import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

tpl = open(os.path.join(HERE, "app_template_v3.html"), encoding="utf-8").read()
bank = json.load(open(os.path.join(HERE, "bank.json"), encoding="utf-8"))

data = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = tpl.replace("__BANK__", data)

out = os.path.join(ROOT, "听力刷题-连做版.html")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

print("out  :", out)
print("size : %.1f KB" % (len(html.encode("utf-8")) / 1024))
print("left :", html.count("__BANK__"))
