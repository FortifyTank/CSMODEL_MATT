import json

def word_count(text):
    return len(text.split())

def check_word_counts():
    with open('CSMODEL.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    total_md_words = 0
    md_cells_over_100 = []
    
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source']).strip()
            # if it starts with # it's a heading, but they still count towards the 5000 word total.
            count = word_count(source)
            total_md_words += count
            
            # They say "Maximum of 100 words per Markdown cell used to describe or explain a code block"
            # It's tricky to know which ones "describe a code block". So let's just find any markdown cell > 100 words.
            if count > 100:
                md_cells_over_100.append((i, count, source[:100]))
                
    print(f"Total Markdown words: {total_md_words}")
    if total_md_words > 5000:
        print("WARNING: Total Markdown words exceed 5,000!")
    else:
        print("Total Markdown words are within the 5,000 limit.")
        
    print(f"\nMarkdown cells over 100 words: {len(md_cells_over_100)}")
    for idx, count, preview in md_cells_over_100:
        print(f"Cell {idx}: {count} words - Preview: {preview}...")

if __name__ == "__main__":
    check_word_counts()
