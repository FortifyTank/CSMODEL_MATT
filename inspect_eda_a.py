import json

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, c in enumerate(nb['cells']):
    source_text = ''.join(c.get('source', []))
    if 'A. Does the distribution of academic burnout risk vary' in source_text or (i >= 58 and i <= 65):
        print(f"--- CELL {i} [{c['cell_type']}] ---")
        print(source_text)
