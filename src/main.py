import shutil
import os


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






main()