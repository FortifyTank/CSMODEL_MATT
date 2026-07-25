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
        elif '6.0 Statistical Inference' in source_text or '6' in source_text[:5]:
            if '6.0' in source_text or '# 6' in source_text:
                current_section = "6"
        elif '7.0 Summary' in source_text or '# 7' in source_text:
            current_section = "7"
            
    if current_section in ["4", "6"]:
        first_line = source_text.split('\n')[0][:150] if source_text else ""
        print(f"[{i:03d}] [{c['cell_type']}] (Sec {current_section}): {first_line.strip()}")
