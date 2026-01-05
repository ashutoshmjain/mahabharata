import re
import os

def create_clean_filename(title, index):
    clean_title = title.replace(" Parva", "").strip()
    filename_part = re.sub(r'[^a-zA-Z0-9\s-]', '', clean_title).lower().replace(' ', '-')
    filename_part = re.sub(r'-+', '-', filename_part)
    return f"{index:02d}-{filename_part}.md"

def split_adi_parva():
    adi_parva_path = 'src/maha01.md'
    output_dir = 'src/adi-parva'
    
    try:
        with open(adi_parva_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Original {adi_parva_path} not found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # This pattern finds a SECTION line, followed by a blank line, then the (Parva) line.
    pattern = re.compile(r"^(SECTION [IVXLC]+)\s*\n\n^\((.+? Parva)\)$", re.MULTILINE)
    
    markers = list(pattern.finditer(content))
    
    if not markers:
        print("Could not find any sub-parva markers with the specified pattern. Aborting.")
        return

    # --- 1. Create the Introduction File ---
    first_parva_start = markers[0].start()
    intro_content = content[:first_parva_start].strip()
    intro_filename = "00-introduction.md"
    intro_filepath = os.path.join(output_dir, intro_filename)
    with open(intro_filepath, 'w', encoding='utf-8') as f:
        f.write(intro_content)
    print(f"Created: {intro_filepath}")

    toc_links = [f"- [Introduction](./adi-parva/{intro_filename})"]

    # --- 2. Create files for each Sub-Parva ---
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
            f.write(sub_content)
        print(f"Created: {filepath}")
        
        clean_name = parva_name.replace(" Parva", "")
        toc_links.append(f"- [{clean_name}](./adi-parva/{filename})")
    
    # --- 3. Create the new maha01.md as a TOC ---
    new_maha01_content = "# Adi Parva\n\nThis is the first book of the Mahabharata. It contains the following sub-parvas:\n\n" + "\n".join(toc_links)
    with open('src/maha01.md', 'w', encoding='utf-8') as f:
        f.write(new_maha01_content)
    print("Updated src/maha01.md with the new table of contents.")

    # --- 4. Update SUMMARY.md ---
    try:
        with open('src/SUMMARY.md', 'r', encoding='utf-8') as f:
            summary_content = f.read()
        
        summary_adi_parva_section = "  - [Adi Parva](./maha01.md)\n"
        for link in toc_links:
            summary_adi_parva_section += f"    {link}\n"
            
        summary_pattern = re.compile(r"(\s*-\s*\[Adi Parva\]\(\./maha01\.md\))")
        new_summary_content, count = summary_pattern.subn(summary_adi_parva_section, summary_content)

        if count > 0:
            with open('src/SUMMARY.md', 'w', encoding='utf-8') as f:
                f.write(new_summary_content)
            print("Updated src/SUMMARY.md with nested Adi Parva chapters.")
        else:
            print("Warning: Could not find Adi Parva entry in src/SUMMARY.md. Navigation not updated.")
    except FileNotFoundError:
        print("Warning: src/SUMMARY.md not found. Could not update navigation.")


if __name__ == "__main__":
    split_adi_parva()
