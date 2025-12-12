import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        # If the file is a folder, recurse
        if os.path.isdir(from_path):
            dest_subdir = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(from_path, template_path, dest_subdir, basepath)
        else:
            # Determine the correct destination HTML path
            if filename == "index.md":
                # Keep folder structure: folder/index.html
                dest_path = os.path.join(dest_dir_path, "index.html")
            else:
                # Convert filename.md -> filename.html
                dest_path = os.path.join(dest_dir_path, Path(filename).with_suffix(".html").name)
            
            # Ensure destination folder exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(from_path, template_path, dest_path, basepath)




def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
