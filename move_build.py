import os
import shutil

# Paths
react_build_path = 'frontend/build'
flask_static_path = 'backend/'  # Remove the extra 'static' at the end
flask_templates_path = 'backend/templates'

def move_build_files():
    # Create static and templates directories if they don't exist
    os.makedirs(flask_static_path, exist_ok=True)
    os.makedirs(flask_templates_path, exist_ok=True)

    # Clear existing contents of static and templates directories
    for item in os.listdir(flask_static_path):
        item_path = os.path.join(flask_static_path, item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # Move build files to static directory
    for item in os.listdir(react_build_path):
        if item != 'index.html':
            s = os.path.join(react_build_path, item)
            d = os.path.join(flask_static_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

    # Move index.html to templates directory
    index_src = os.path.join(react_build_path, 'index.html')
    index_dest = os.path.join(flask_templates_path, 'index.html')
    shutil.copy2(index_src, index_dest)

    print("React build files have been successfully moved to Flask directories.")

if __name__ == "__main__":
    move_build_files()