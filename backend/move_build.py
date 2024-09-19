import os
import shutil

# Paths
react_build_path = '../frontend/build'  # Adjust this path as needed
flask_static_path = 'static'
flask_templates_path = 'templates'

# Create static and templates directories if they don't exist
os.makedirs(flask_static_path, exist_ok=True)
os.makedirs(flask_templates_path, exist_ok=True)

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
shutil.copy2(os.path.join(react_build_path, 'index.html'), flask_templates_path)

print("React build files have been successfully moved to Flask directories.")