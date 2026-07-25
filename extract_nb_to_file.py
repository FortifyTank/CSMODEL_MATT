import json

def extract_notebook():
    with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    with open('notebook_extracted.txt', 'w', encoding='utf-8') as out:
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'markdown':
                source = ''.join(cell['source']).strip()
                out.write(f'--- CELL {i} (Markdown) ---\n')
                out.write(source + '\n\n')
            elif cell['cell_type'] == 'code':
                source = ''.join(cell['source']).strip()
                if '5.' in source or 'Mining' in source or 'Apriori' in source or 'KMeans' in source or 'K-Means' in source or 'association' in source or 'rule' in source or 'cluster' in source:
                    out.write(f'--- CELL {i} (Code - Section 5 related) ---\n')
                    out.write(source + '\n\n')
                elif 'def' in source and '5' in source:
                    out.write(f'--- CELL {i} (Code) ---\n')
                    out.write(source + '\n\n')

if __name__ == "__main__":
    extract_notebook()
