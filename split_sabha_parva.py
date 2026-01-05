import re
import os

def create_clean_filename(title, index):
    clean_title = title.replace(" Parva", "").strip()
    filename_part = clean_title.lower().replace(' ', '-').replace('_', '-')
    filename_part = re.sub(r'[^a-z0-9-]', '', filename_part)
    return f"{index:02d}-{filename_part}.md"

def process_and_structure_content(content_block, parva_name=None):
    # Remove existing main titles if they exist to avoid duplication
    content_block = re.sub(r'^# The Mahabharata.*?\n', '', content_block, flags=re.MULTILINE)
    content_block = re.sub(r'^## SABHA PARVA.*?\n', '', content_block, flags=re.MULTILINE)

    # Add a main title based on the parva name
    if parva_name and not content_block.strip().startswith('#'):
        content_block = f"# {parva_name}\n\n{content_block}"

    # Convert 'SECTION X' to level 2 headings
    content_block = re.sub(r'^(SECTION [IVXLC]+)', r'## \1', content_block, flags=re.MULTILINE)

    # Clean up excessive newlines that might result from substitutions
    content_block = re.sub(r'\n{3,}', '\n\n', content_block)
    
    # Add footnote
    footnote = "\n\n---\n*Editor's Note: This text has been reviewed for major typos and grammatical errors. Headings and subheadings have been introduced to improve readability, but the original text remains otherwise unaltered.*"
    
    if footnote not in content_block:
        content_block += footnote
        
    return content_block.strip()

def run_split_sabha():
    original_file = 'src/maha02.md'
    output_dir = 'src/sabha-parva'
    
    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Could not read {original_file}")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    # Pattern to find '(Y Parva)' on its own line, possibly preceded by a section line.
    # This marks the beginning of a new sub-parva.
    pattern = re.compile(r"^(SECTION [IVXLC]+.*?)\n\n(.+? Parva)", re.MULTILINE)
    
    markers = list(pattern.finditer(content))
    
    if not markers:
        print("No sub-parva markers found. Cannot split.")
        return
        
    toc_links = []
    summary_links = []

    # --- 1. Introduction File (if any content exists before first marker) ---
    first_parva_start = markers[0].start()
    if first_parva_start > 0:
        intro_content = content[:first_parva_start].strip()
        intro_filename = "00-sabha-parva-intro.md"
        intro_filepath = os.path.join(output_dir, intro_filename)
        
        with open(intro_filepath, 'w', encoding='utf-8') as f:
            f.write(process_and_structure_content(intro_content, "Sabha Parva Introduction"))
        print(f"Created: {intro_filepath}")
        toc_links.append(f"- [Introduction](./sabha-parva/{intro_filename})")
        summary_links.append(f"    - [Introduction](./sabha-parva/{intro_filename})")

    # --- 2. Sub-Parva Files ---
    for i in range(len(markers)):
        current_marker = markers[i]
        parva_name = current_marker.group(2)
        start_pos = current_marker.start()
        
        end_pos = len(content)
        if i + 1 < len(markers):
            end_pos = markers[i+1].start()
            
        sub_content = content[start_pos:end_pos].strip()
        filename = create_clean_filename(parva_name, i + 1)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(process_and_structure_content(sub_content, parva_name))
        print(f"Created: {filepath}")
        
        clean_name = parva_name.replace(" Parva", "")
        toc_links.append(f"- [{clean_name}](./sabha-parva/{filename})")
        summary_links.append(f"    - [{clean_name}](./sabha-parva/{filename})")
    
    # --- 3. New maha02.md (Table of Contents) ---
    new_maha02_content = "# Sabha Parva\n\nThis is the second book of the Mahabharata. It contains the following sub-parvas:\n\n" + "\n".join(toc_links)
    with open('src/maha02.md', 'w', encoding='utf-8') as f:
        f.write(new_maha02_content)
    print("Updated src/maha02.md with the new table of contents.")

    # --- 4. Update SUMMARY.md ---
    try:
        with open('src/SUMMARY.md', 'r', encoding='utf-8') as f:
            summary_lines = f.readlines()
        
        new_summary_lines = []
        in_section = False
        for line in summary_lines:
            # Add the current line first
            new_summary_lines.append(line)
            # If this is the line for Sabha Parva, inject the new sub-chapters
            if '[Sabha Parva]' in line:
                new_summary_lines.extend([s + '\n' for s in summary_links])

        with open('src/SUMMARY.md', 'w', encoding='utf-8') as f:
            f.writelines(new_summary_lines)
        print("Updated src/SUMMARY.md with nested Sabha Parva chapters.")
    except FileNotFoundError:
        print("Warning: src/SUMMARY.md not found.")

if __name__ == "__main__":
    run_split_sabha()
