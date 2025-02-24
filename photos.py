import streamlit as st
import os
from PIL import Image, ImageOps
import random
import pillow_heif
import requests
from dotenv import load_dotenv
from github import Github
from github import Auth

load_dotenv()

# Register HEIF opener with PIL
pillow_heif.register_heif_opener()

def get_repo_tags():
    auth = Auth.Token(os.getenv("GITHUB_API_KEY"))
    g = Github(auth=auth)
    repo = g.get_repo(os.getenv("GITHUB_REPO"))
    contents = repo.get_contents("")
    for content_file in contents:
        print(content_file)
    return [content_file.name for content_file in contents if content_file.type == "dir"]

st.set_page_config(
    page_title="Amy&Zach's Photo Wall",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="collapsed"
)
tags = get_repo_tags()
_, page_col, _ = st.columns([0.1, 0.8, 0.1], vertical_alignment="bottom")
# _, header_col, button_col, _  = st.columns([0.1, 0.6, 0.1, 0.1], vertical_alignment="bottom")
with page_col:
    st.header("📷 Amy&Zach's Photo Wall 🎈")
    selection = st.segmented_control(
        label = None, options = tags, selection_mode="single",
        default = tags[0]
    )


# Get the path to the images folder
image_folder = os.path.join(os.path.dirname(__file__), 'images')

# List all image files
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic'))]

# Add random button
# if random_button:
#     selected_images = random.sample(image_files, min(9, len(image_files)))
# else:
selected_images = random.sample(image_files, min(9, len(image_files)))

# Calculate image heights and distribute them evenly across columns
image_data = []
for image_file in selected_images:
    image_path = os.path.join(image_folder, image_file)
    try:
        with Image.open(image_path) as img:
            img = ImageOps.exif_transpose(img)
            image_data.append((image_file, img.size[1] / img.size[0]))  # Store aspect ratio
    except Exception as e:
        st.error(f"Could not load image: {image_file}")

# Distribute images across columns to balance heights
columns_data = [[], [], []]  # Three columns
column_heights = [0, 0, 0]

for image_file, aspect_ratio in image_data:
    # Find the column with minimum height
    min_height_col = column_heights.index(min(column_heights))
    columns_data[min_height_col].append(image_file)
    column_heights[min_height_col] += aspect_ratio

# Display images in balanced columns
_, wall, _ = st.columns([0.15, 0.7, 0.15])
with wall:
    cols = st.columns(3)
    for col_idx, column_images in enumerate(columns_data):
        with cols[col_idx]:
            for image_file in column_images:
                image_path = os.path.join(image_folder, image_file)
                try:
                    image = Image.open(image_path)
                    image = ImageOps.exif_transpose(image)
                    st.image(image, caption=None, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not load image: {image_file}")
    random_button = st.button("Random Load")
