import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the posts folder
posts_dir = os.path.join(script_dir, 'posts')

# List all files in the posts folder
try:
    files = os.listdir(posts_dir)
except FileNotFoundError:
    print("Posts folder not found.")
    files = []

print("Files in posts folder:")
for f in files:
    print(f)

print(f"Total count: {len(files)}")
