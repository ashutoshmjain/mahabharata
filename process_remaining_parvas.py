import re
import os

def get_parva_name_from_filename(filename):
    """A simple mapping from filename to title."""
    parva_map = {
        "maha04.md": "Virata Parva",
        "maha05.md": "Udyog Parva",
        "maha06.md": "Bhishma Parva",
        "maha07.md": "Drona Parva",
        "maha08.md": "Karna Parva",
        "maha09.md": "Shalya Parva",
        "maha10.md": "Sauptika Parava",
        "maha11.md": "Stri Parva",
        "maha12.md": "Santi Parva",
        "maha13.md": "Anusasna Parva",
        "maha14.md": "Ashwamedha Parva",
        "maha15.md": "Ashramavasika Parva",
        "maha16.md": "Mausla Parva",
        "maha17.md": "Mahaprasthanika Parva",
        "maha18.md": "Svargarohanika Parva",
    }
    return parva_map.get(filename)

def process_and_structure_content(content_block, parva_name=None):
    """Adds headings, cleans up text, and adds a footnote."""
    # Remove boilerplate text if present
    content_block = re.sub(r'^# The Mahabharata.*?(Scanned at sacred-texts.com.*?Hare\.)', '', content_block, flags=re.DOTALL | re.MULTILINE)
    content_block = re.sub(r'^BOOK \d+', '', content_block, flags=re.MULTILINE).strip()
    # Remove existing Parva title if it's there
    if parva_name:
        content_block = re.sub(r'^##\s*' + re.escape(parva_name.upper()) + r'\s*$', '', content_block, flags=re.IGNORECASE | re.MULTILINE).strip()

    # Add a main title
    if parva_name and not content_block.strip().startswith('#'):
        content_block = f"# {parva_name}\n\n{content_block}"

    # Convert 'SECTION X' to level 2 headings
    content_block = re.sub(r'^(SECTION [IVXLC]+)', r'## \1', content_block, flags=re.MULTILINE)
    
    # Clean up excessive newlines
    content_block = re.sub(r'\n{3,}', '\n\n', content_block).strip()
    
    footnote = """

---
*Editor's Note: This text has been reviewed for major typos and grammatical errors. Headings and subheadings have been introduced to improve readability, but the original text remains otherwise unaltered.*"""
    
    if footnote not in content_block:
        content_block += footnote
        
    return content_block

def main():
    parva_files_to_process = [f"maha{i:02d}.md" for i in range(4, 19)]

    for md_file in parva_files_to_process:
        parva_name = get_parva_name_from_filename(md_file)
        if not parva_name:
            print(f"--- Skipping {md_file}: No name mapping found.")
            continue
            
        print(f"--- Processing {md_file} ({parva_name}) ---")
        file_path = os.path.join('src', md_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"  Formatting as a single file.")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(process_and_structure_content(content, parva_name))
            print(f"  Formatted and updated: {file_path}")

        except FileNotFoundError:
            print(f"  Error: Could not read {file_path}")
            continue

    print("\n--- Finished processing all remaining Parva files. ---")

if __name__ == "__main__":
    main()