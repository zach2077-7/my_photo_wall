import streamlit as st
import os
from PIL import Image, ImageOps

st.title("Photo wall")

# Get the path to the images folder
image_folder = os.path.join(os.path.dirname(__file__), 'images')

# List all image files
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic'))]

# Display images in a grid
cols = st.columns(3)
for idx, image_file in enumerate(image_files):
    with cols[idx % 3]:
        image_path = os.path.join(image_folder, image_file)
        image = Image.open(image_path)
        image = ImageOps.exif_transpose(image)  # This preserves the original orientation
        st.image(image, caption=None, use_container_width=True)

