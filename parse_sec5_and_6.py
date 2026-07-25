import json

with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

current_section = ""
for c in nb['cells']:
    source_text = ''.join(c.get('source', []))
    
    if c['cell_type'] == 'markdown':
        if '5.0 Data Mining' in source_text:
            current_section = "5"
        elif '6.0 Statistical Inference' in source_text or '6' in source_text[:5]:
            # Try to guess if it's section 6
            if '6.0' in source_text or '# 6' in source_text:
                current_section = "6"
        elif '7.0 Summary' in source_text or '# 7' in source_text:
            current_section = "7"
            
    if current_section == "5":
        print(f"--- [SEC 5: {c['cell_type']}] ---")
        print(source_text[:2000]) # truncated to avoid blowing up output
