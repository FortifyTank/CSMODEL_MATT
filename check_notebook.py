import json
import re

try:
    with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)
except Exception as e:
    print("Error reading notebook:", e)
    exit()

markdown_headers = []
code_snippets = []

for cell in nb.get('cells', []):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        headers = re.findall(r'^#+ .*$', source, re.MULTILINE)
        markdown_headers.extend(headers)
    elif cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if any(keyword in source for keyword in ['sklearn', 'scipy', 'statsmodels', 'cluster', 'kmeans', 'ttest', 'apriori', 'fpgrowth', 'corr']):
            code_snippets.append(source)

print("--- MARKDOWN HEADERS ---")
for h in markdown_headers:
    print(h)

print("\n--- CODE MATCHING MCO2 KEYWORDS ---")
for i, code in enumerate(code_snippets):
    lines = code.split('\n')
    print(f"Code block {i+1}:")
    for line in lines:
        if any(keyword in line for keyword in ['sklearn', 'scipy', 'statsmodels', 'cluster', 'kmeans', 'ttest', 'apriori', 'fpgrowth', 'corr']):
            print(f"  {line.strip()}")
