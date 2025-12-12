import os
import shutil

def copy_files_recursive(src, dst):
    # Create destination directory if it does not exist
    if not os.path.exists(dst):
        os.makedirs(dst)

    # Loop through all items in src
    for name in os.listdir(src):
        source_path = os.path.join(src, name)
        dest_path = os.path.join(dst, name)

        # Log action
        print(f" * {source_path} -> {dest_path}")

        # If file → copy it
        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)

        # If directory → recurse
        else:
            copy_files_recursive(source_path, dest_path)
