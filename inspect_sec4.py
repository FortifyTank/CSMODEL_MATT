import json

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

current_section = ""
for i, c in enumerate(nb['cells']):
    source_text = ''.join(c.get('source', []))
    
    if c['cell_type'] == 'markdown':
        if '# 4.0' in source_text or '# 4 ' in source_text:
            current_section = "4"
        elif '5.0 Data Mining' in source_text:
            current_section = "5"
            
    if current_section == "4":
        print(f"--- CELL {i} [{c['cell_type']}] ---")
        print(source_text)
