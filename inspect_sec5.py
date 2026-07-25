import json

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, c in enumerate(nb['cells']):
    source_text = ''.join(c.get('source', []))
    if '5.' in source_text or 'Apriori' in source_text or 'Data Mining' in source_text or (i >= 75 and i <= 90):
        print(f"--- CELL {i} [{c['cell_type']}] ---")
        print(source_text[:300])
