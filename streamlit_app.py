import streamlit as st
import pandas as pd
from PIL import Image
import cv2
import numpy as np

# Load color dataset (colors.csv should have columns: color, R, G, B)
csv_file = 'colors.csv'
df = pd.read_csv(csv_file)

# Function to get the closest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color"]
    return cname

st.title("Image Color Detection App")
st.write("Upload an image, click to detect a color, and see the color name, RGB values, and color box.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png","jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='https://sl.bing.net/hC1OaODIfzE', use_column_width=True)
    
    st.write("Click on the image to detect color.")
    
    # Convert image to OpenCV format
    image_cv = np.array(image)
    if image_cv.shape[2] == 4:  # handle alpha channel
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGBA2RGB)
    
    # Click button to detect color
    if st.button("Detect Color"):
        # Resize image to 1x1 to get average color
        avg_color = cv2.resize(image_cv, (1, 1), interpolation=cv2.INTER_AREA)[0,0]
        R, G, B = int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
        color_name = get_color_name(R, G, B)
        
        st.write(f"**Color Name:** {color_name}")
        st.write(f"**RGB Values:** R={R}, G={G}, B={B}")
        
        # Display color box
        st.markdown(
            f"<div style='width:100px; height:50px; background-color:rgb({R},{G},{B});'></div>",
            unsafe_allow_html=True
        )

   
