import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Free AI Tool Suite", layout="wide")
st.title("🛠️ My Custom AI Tool")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    tab1, tab2 = st.tabs(["🚀 App Builder", "📹 Video Architect"])

    with tab1:
        st.header("Base44-Style App Builder")
        desc = st.text_area("Describe an app to build:")
        if st.button("Generate Code"):
            res = model.generate_content(f"Act as a coder. Write Python/Streamlit code for: {desc}")
            st.code(res.text)

    with tab2:
        st.header("Image-to-Video Prompter")
        file = st.file_uploader("Upload an image", type=["jpg", "png"])
        if file:
            img = Image.open(file)
            st.image(img, width=300)
            if st.button("Get Motion Prompt"):
                res = model.generate_content(["Create a 5-second cinematic motion prompt for this image.", img])
                st.info(res.text)
else:
    st.warning("Please enter your API Key in the sidebar.")
