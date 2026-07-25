import json

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i in range(50, 62):
    if i < len(nb['cells']):
        c = nb['cells'][i]
        print(f"--- Cell {i} [{c['cell_type']}] ---")
        print(''.join(c.get('source', [])))
