import json

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

in_sec6 = False
for i, c in enumerate(nb['cells']):
    source_text = ''.join(c.get('source', []))
    
    if c['cell_type'] == 'markdown':
        if '# 6.0 Statistical Inference' in source_text or '6.0 Hypothesis Testing' in source_text:
            in_sec6 = True
        elif '# 7.0' in source_text or '# References' in source_text:
            in_sec6 = False
            
    if in_sec6:
        print(f"--- CELL {i} [{c['cell_type']}] ---")
        print(source_text)
