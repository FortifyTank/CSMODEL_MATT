import json
with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

in_sec5 = False
for c in nb['cells']:
    source_text = ''.join(c.get('source', []))
    if c['cell_type'] == 'markdown' and '5.0 Data Mining' in source_text:
        in_sec5 = True
    
    if in_sec5:
        print(f"[{c['cell_type']}]")
        print(source_text)
        print("---")
