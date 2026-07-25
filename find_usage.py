import json
import re

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        source = ''.join(c.get('source', []))
        if 'processed_df' in source or 'scaler' in source or 'label_enc' in source:
            print(f"--- Code Cell {i} matches ---")
            print(source[:500])
