import os
import re

def get_parva_title(filename):
    """A simple mapping from filename to title."""
    parva_map = {
        "maha00.md": "Mahabharata",
        "maha01.md": "Adi Parva",
        "maha02.md": "Sabha Parva",
        "maha03.md": "Vana Parva",
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
        "how.md": "About"
    }
    return parva_map.get(filename)

def get_sub_parva_title(filename):
    """Creates a clean title from a sub-parva filename."""
    # "01-paushya.md" -> "Paushya"
    name = os.path.splitext(filename)[0]
    name = re.sub(r'^\d\d-', '', name) # remove number prefix
    name = name.replace('-', ' ').replace('_', ' ')
    return name.title()


def build_summary():
    src_dir = 'src'
    summary_content = "# Summary\n\n"
    
    # Define the order of the main files
    main_files = [f"maha{i:02d}.md" for i in range(19)]
    main_files.append("how.md")

    # Entry for Mahabharata (Cover)
    summary_content += f"- [{get_parva_title('maha00.md')}]('./{ 'maha00.md' }')\n"
    
    for main_file in main_files[1:]: # Start from maha01.md
        parva_name = get_parva_title(main_file)
        if not parva_name:
            continue
            
        summary_content += f"  - [{parva_name}](./{main_file})\n"
        
        # Check if there is a corresponding subdirectory for sub-parvas
        dir_name = parva_name.lower().replace(' ', '-')
        sub_parva_dir = os.path.join(src_dir, dir_name)
        
        if os.path.isdir(sub_parva_dir):
            sub_files = sorted([f for f in os.listdir(sub_parva_dir) if f.endswith('.md')])
            for sub_file in sub_files:
                sub_title = get_sub_parva_title(sub_file)
                summary_content += f"    - [{sub_title}](./{dir_name}/{sub_file})\n"
                
    summary_filepath = os.path.join(src_dir, 'SUMMARY.md')
    with open(summary_filepath, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    print(f"Successfully rebuilt {summary_filepath}")

if __name__ == "__main__":
    build_summary()
