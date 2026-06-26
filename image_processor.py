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
    # 2. Let the user choose the output format
    output_format = st.selectbox("Select desired output format:", ["PNG", "JPG", "JPEG"])
    
    # Map the selection to Pillow's format requirements and MIME types
    pil_format = "JPEG" if output_format in ["JPG", "JPEG"] else "PNG"
    mime_type = "image/jpeg" if output_format in ["JPG", "JPEG"] else "image/png"
    file_extension = output_format.lower()

    try:
        # 3. Process image live in memory using Pillow
        img = Image.open(uploaded_file)
        
        # 4. Format-specific grayscale and transparency conversion
        if output_format == "PNG":
            # "LA" keeps the transparent background intact for PNGs
            img_gray = img.convert("LA")
        else:
            # JPEGs don't support transparency. We apply a white background if needed.
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # Create a solid white background matching the image size
                white_bg = Image.new("RGB", img.size, (255, 255, 255))
                # Paste the logo onto the white background using its own transparency as a mask
                white_bg.paste(img, (0, 0), img.convert("RGBA").split()[3])
                img_gray = white_bg.convert("L")
            else:
                img_gray = img.convert("L")

        img_resized = img_gray.resize((512, 512), Image.Resampling.LANCZOS)
        
        # Display instant visual layout previews side-by-side
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Original Upload", use_container_width=True)
        with col2:
            st.image(img_resized, caption=f"Processed (512x512 Grayscale {output_format})", use_container_width=True)

        # 5. Save processed image array bytes for the download handler
        img_buffer = BytesIO()
        img_resized.save(img_buffer, format=pil_format)
        img_bytes = img_buffer.getvalue()

        # 6. Generate the exact Base64 string data based on the chosen format
        processed_base64 = base64.b64encode(img_bytes).decode("utf-8")

        st.success("✨ Processing successful!")

        # 7. Native web download interaction layer
        st.download_button(
            label=f"📥 Download Processed {output_format} File",
            data=img_bytes,
            file_name=f"processed_output.{file_extension}",
            mime=mime_type
        )
        
        # Clickable dropdown layout box containing the raw text string
        with st.expander("📋 Click here to reveal Base64 Text Code String"):
            st.code(processed_base64, language="text")

    except Exception as e:
        st.error(f"Error processing image asset: {e}")
