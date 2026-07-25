import json

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, c in enumerate(nb.get('cells', [])):
    source_text = ''.join(c.get('source', []))
    if 'pearson' in source_text.lower() or 'chi2' in source_text.lower() or 'tukey' in source_text.lower() or 'anova' in source_text.lower():
        print(f"--- CELL {i} [{c['cell_type']}] ---")
        print(source_text[:300])
