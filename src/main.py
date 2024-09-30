import shutil
import os
from markdown_blocks import markdown_to_html_node


def main():
    copy_static_to_public()
    pass

def copy_static_to_public():

    public_path = "./public"
    static_path = "./static"

    # delete full public directory and then reinstate (clears all files)
    if os.path.exists(public_path):
        print("Deleting ./public folder and contents")
        shutil.rmtree(public_path)
    os.mkdir("./public/")

    source_directory = static_path
    destination_directory = public_path

    copy_folder(source_directory, destination_directory)

    source_file = "./content/index.md"
    template_file = "./template.html"
    destination_file = "./public/index.html"
    #generate_page(source_file, template_file, destination_file)
    generate_pages_recursive("./content", "./", "./public")





def copy_folder(source_dir, destination_dir):
    current_contents = os.listdir(source_dir)
    for item in current_contents:
        item_path = os.path.join(source_dir, item)

        # if current item is folder, go deeper
        if not os.path.isfile(item_path):
            new_dest_dir = os.path.join(destination_dir, item)
            os.mkdir(new_dest_dir)
            print(f"Making new folder at {new_dest_dir}")
            copy_folder(item_path, new_dest_dir)
            print(f"Returning to {source_dir}")

        # otherwise we have a file, just copy it over normally
        else:
            shutil.copy(item_path, destination_dir)
            print(f"Copying {item_path} to {destination_dir}")

    print(f"Finished copying folder {source_dir} to {destination_dir}")       

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if (line[0:2]) == "# ":
            return line[2:].strip()
    
    raise Exception("No h1 header in markdown file")

def generate_page(from_path, template_path, dest_path):
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path).read()
    template = open(template_path).read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("No source directory present")
    
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    contents = os.listdir(dir_path_content)

    for item in contents:
        item_path = os.path.join(dir_path_content, item)

        if not os.path.isfile(item_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            os.mkdir(new_dest_dir)
            generate_pages_recursive(item_path, template_path, new_dest_dir)

        else:
            filename = item.removesuffix(".md")
            print(f"Generating {dest_dir_path}/{filename}.html from {dir_path_content}/{filename}.md")
            
            template = open(template_path+"template.html").read()
            md = open(os.path.join(dir_path_content, item)).read()
            html = markdown_to_html_node(md).to_html()
            title = extract_title(md)
            
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            
            with open(f"{dest_dir_path}/{filename}.html", "w") as f:
                f.write(template)


    

    




main()