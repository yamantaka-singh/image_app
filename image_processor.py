import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Set up page configurations
st.set_page_config(page_title="Logo Processor", page_icon="🖼️", layout="centered")

st.title("🖼️ Instant Logo Processing Engine")
st.write("Upload your image. The engine will instantly resize it to 512x512, make it grayscale, and generate your string code.")

# 1. Drag and drop file uploader
uploaded_file = st.file_uploader("Drop your logo image here...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    try:
        # 2. Process image live in memory using Pillow
        img = Image.open(uploaded_file)
        img_gray = img.convert("L")
        img_resized = img_gray.resize((512, 512), Image.Resampling.LANCZOS)
        
        # Display instant visual layout previews side-by-side
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Original Upload", use_container_width=True)
        with col2:
            st.image(img_resized, caption="Processed (512x512 Grayscale)", use_container_width=True)

        # 3. Save processed image array bytes for the download handler
        img_buffer = BytesIO()
        img_resized.save(img_buffer, format="PNG")
        img_bytes = img_buffer.getvalue()

        # 4. Generate the exact Base64 string data
        processed_base64 = base64.b64encode(img_bytes).decode("utf-8")

        st.success("✨ Processing successful!")

        # 5. Native web download interaction layer
        st.download_button(
            label="📥 Download Processed Image File",
            data=img_bytes,
            file_name="processed_output.png",
            mime="image/png"
        )
        
        # Clickable dropdown layout box containing the raw text string
        with st.expander("📋 Click here to reveal Base64 Text Code String"):
            st.code(processed_base64, language="text")

    except Exception as e:
        st.error(f"Error processing image asset: {e}")