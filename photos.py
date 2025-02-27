import streamlit as st
import random
import pillow_heif
import requests
from storage import get_tags, get_images, load_image
from PIL import Image, ImageOps
from io import BytesIO

# Register HEIF opener with PIL
pillow_heif.register_heif_opener()

st.set_page_config(
    page_title="Amy&Zach's Photo Wall",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="collapsed"
)
tags = get_tags()
images = { tag : get_images(tag) for tag in tags}
print(images)
_, page_col, _ = st.columns([0.1, 0.8, 0.1], vertical_alignment="top")
# _, header_col, button_col, _  = st.columns([0.1, 0.6, 0.1, 0.1], vertical_alignment="bottom")
with page_col:
    st.header("📷 Amy&Zach's Photo Wall 🎈")
    selection = st.segmented_control(
        label = None, options = tags, 
        selection_mode="single",
        default = tags[0]
    )


selected_images = random.sample(images[selection], min(9, len(images[selection])))

# Calculate image heights and distribute them evenly across columns
image_data = []
for image_url in selected_images:
    try:
        img = load_image(image_url)
        img = ImageOps.exif_transpose(img)
        image_data.append((image_url, img.size[1] / img.size[0]))  # Store aspect ratio
    except Exception as e:
        print(f"Error loading image {image_url}: {e}")
        st.error(f"Could not load image: {image_url}")

# Distribute images across columns to balance heights
columns_data = [[], [], []]  # Three columns
column_heights = [0, 0, 0]

for image_url, aspect_ratio in image_data:
    # Find the column with minimum height
    min_height_col = column_heights.index(min(column_heights))
    columns_data[min_height_col].append(image_url)
    column_heights[min_height_col] += aspect_ratio

# Display images in balanced columns
_, wall, _ = st.columns([0.15, 0.7, 0.15])
with wall:
    cols = st.columns(3)
    for col_idx, column_images in enumerate(columns_data):
        with cols[col_idx]:
            for image_url in column_images:
                try:
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    image = ImageOps.exif_transpose(image)
                    st.image(image, caption=None, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not load image: {image_url}")
    random_button = st.button("Random Load")
