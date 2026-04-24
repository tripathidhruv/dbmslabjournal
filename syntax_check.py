import re

text = open("index.html.bak", "r", encoding="utf-8").read()

# Extract the PRACTICALS javascript block
import sys
m = re.search(r'const PRACTICALS = \[.*?\];', text, re.DOTALL)
if not m:
    print("Could not find PRACTICALS array")
    sys.exit()

js_code = m.group(0)

# We want to find common syntax errors. We'll simply print it out and look or find misplaced colons.
# Let's count the number of { and }.
print("Checking brackets in PRACTICALS")
print(f"{{ count: {js_code.count('{')}")
print(f"}} count: {js_code.count('}')}")
print(f"[ count: {js_code.count('[')}")
print(f"] count: {js_code.count(']')}")
print(f"` count: {js_code.count('`')}")
print(f"\" count: {js_code.count(chr(34))}")

# Check lines that contain 'viva:' to ensure they are fine
for i, line in enumerate(js_code.split('\n')):
    if 'viva:' in line:
        if not line.strip().endswith('}'):
             if not line.strip().endswith('},'):
                 print(f"Suspicious viva line: {line.strip()}")
