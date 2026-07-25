import json

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

in_sec33 = False
for i, c in enumerate(nb['cells']):
    source_text = ''.join(c.get('source', []))
    
    if c['cell_type'] == 'markdown':
        if '## 3.3 Data Pre-processing' in source_text:
            in_sec33 = True
        elif '# 4.0' in source_text:
            in_sec33 = False
            
    if in_sec33:
        if c['cell_type'] == 'markdown':
            print(f"[{c['cell_type']}] {source_text[:200]}")
        else:
            print(f"[{c['cell_type']}]")
            print(source_text[:300])
            print("...")
