"""Print the rule-examples.html recipes as one rules.toml, so it can be checked against the app's schema."""
import html
import re
import sys
import tomllib

page = open(sys.argv[1] if len(sys.argv) > 1 else "rule-examples.html").read()
blocks = [
    html.unescape(re.sub(r"<[^>]+>", "", block))
    for block in re.findall(r"<b>rules.toml</b></div>\s*<pre[^>]*><code>(.*?)</code></pre>", page, re.S)
]
lists, rules = [], []
for block in blocks:
    # Recipes that introduce a list start with their own [lists] table; one file may hold only one
    lists_table = re.match(r"\[lists\]\n((?:.+\n)+)\n", block)
    if lists_table:
        lists.append(lists_table.group(1))
        block = block[lists_table.end():]
    rules.append(block)
combined = "[lists]\n" + "".join(lists) + "\n" + "\n\n".join(rules) + "\n"

names = [rule["name"] for rule in tomllib.loads(combined)["rules"]]
assert len(names) == len(set(names)), "rule names must be unique across recipes"
print(combined, end="")
