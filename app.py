import streamlit as st
from PIL import Image
import zipfile
import io

from ImageProcessor import ImageProcessor

st.set_page_config(page_title="📸✨ SnapFlip", layout="wide")



st.markdown(
    """
    <h1 style='text-align: center;'>📸✨ SnapFlip</h1>
    <h4 style='text-align: center; color: #6c757d;'>Negative Image Enhancer</h4>
    """,
    unsafe_allow_html=True
)
with st.container():
    with st.expander("About 📸✨ Snapflip"):
        st.markdown(
            """
            <div style=" padding: 20px; margin-bottom: 20px;">
                <p>
                    <strong>SnapFlip</strong> is a streamlined tool designed to effortlessly convert photographic negatives into vivid positive images. Whether you’re digitizing old film, restoring family memories, or enhancing creative projects, SnapFlip makes the process simple and intuitive.
                </p>
                <ul>
                    <li><strong>Batch Upload & Processing:</strong> Easily upload multiple negatives in popular formats (JPG, PNG, TIFF, BMP).</li>
                    <li><strong>Instant Conversion:</strong> Advanced algorithms invert colors and restore your images to their true, positive form.</li>
                    <li><strong>Custom Enhancements:</strong> Fine-tune brightness and contrast to achieve the perfect look.</li>
                    <li><strong>Side-by-Side Comparison:</strong> View original negatives and enhanced positives together for quick evaluation.</li>
                    <li><strong>Bulk Download:</strong> Export all processed images in a convenient ZIP file.</li>
                </ul>
                <p>
                    <em>SnapFlip empowers photographers, archivists, and enthusiasts to breathe new life into old negatives—no technical expertise required. With a clean interface and fast results, it’s the easiest way to unlock the stories hidden in your film.</em>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
info_area=st.empty()
download_area=st.container()
mcol1,mcol2=st.columns([1,1])
# Sidebar controls
with mcol1.container():
    st.header("Controls")
    uploaded_files = st.file_uploader(
        "Upload negative images",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        accept_multiple_files=True
    )
    brightness = st.slider("Adjust Brightness", 0.5, 2.0, 1.0, 0.05)
    contrast = st.slider("Adjust Contrast", 0.5, 2.0, 1.0, 0.05)
    # st.markdown("---")


processed_files = []

if uploaded_files:
    processor = ImageProcessor(brightness=brightness, contrast=contrast)
    zip_buf = io.BytesIO()

    for uploaded_file in uploaded_files:
        try:
            image = Image.open(uploaded_file)
            positive_img = processor.process(image)
            img_bytes = processor.get_bytes(positive_img)
            processed_files.append((f"positive_{uploaded_file.name}.png", img_bytes))
            st.toast(f"{uploaded_file.name}: Processed successfully!")
        except Exception as e:
            st.error(f"{uploaded_file.name}: Error opening file ({e})")
            continue

    if processed_files:
        with zipfile.ZipFile(zip_buf, "w") as zipf:
            for fname, file_bytes in processed_files:
                zipf.writestr(fname, file_bytes)
        zip_buf.seek(0)
        with download_area:
            st.download_button(
                label="Download processed image in a ZIP file",
                data=zip_buf,
                file_name="processed_images.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )

    with mcol2.container():
        st.header("Output")
        for idx, uploaded_file in enumerate(uploaded_files):
            with st.expander(f"{uploaded_file.name}"):
                try:
                    image = Image.open(uploaded_file)
                    positive_img = processor.process(image)
                except Exception as e:
                    st.error(f"Cannot process {uploaded_file.name}: {e}")
                    continue

                col1, col2 = st.columns(2)
                with col1:
                    st.image(image, caption="Original (Negative)", use_container_width=True)
                with col2:
                    st.image(positive_img, caption="Positive (Enhanced)", use_container_width=True)
else:
    info_area.info("Please upload one or more negative images to begin.")

st.markdown(
    """
    <hr style="margin-top: 40px; margin-bottom: 10px;">
    <div style="text-align: center; color: #888;">
        <p>
            Made with ❤️ by <strong>Rahul Dubey</strong> &nbsp;|&nbsp;
            <a href="https://github.com/d-evil0per/snapflip" target="_blank" style="color: #117a65; text-decoration: none;">
                <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="20" style="vertical-align: middle; margin-right: 5px;">
                GitHub
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)