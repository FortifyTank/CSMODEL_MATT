import json

def extract_notebook():
    with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source']).strip()
            print(f'--- CELL {i} (Markdown) ---')
            print(source[:500] + ('...' if len(source) > 500 else ''))
            print()
        elif cell['cell_type'] == 'code':
            source = ''.join(cell['source']).strip()
            # We want to see section 5 and 6 and 7 in more detail, maybe?
            # Let's print the outputs of code cells if they look important or just print a summary
            pass

if __name__ == "__main__":
    extract_notebook()
