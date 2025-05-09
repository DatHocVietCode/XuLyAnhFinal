import cv2
import numpy as np
import streamlit as st

from library import Chapter3 as c3  # Module xử lý ảnh của bạn

st.set_page_config(page_title="Chương 3")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://moewalls.com/wp-content/uploads/2021/11/bliss-tree-thumb-728x410.jpg");
        background-size: cover;
        background-position: center;
        color: black;
    }
    
    .title {
        color: white;
        font-size: 3em;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 5px black;
    }
    .subtitle {
        color: white;
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 2em;
        text-shadow: 1px 1px 3px black;
    }
    .section-title {
        color: white;
        font-size: 1.2em;
        margin-bottom: 0.5em;
        text-shadow: 1px 1px 2px black;
    }
    .info {
        color: white;
        font-size: 1em;
        margin-bottom: 1em;
        text-shadow: 1px 1px 2px black;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Làm cho sidebar trong suốt và chữ màu đen */
    [data-testid="stSidebar"] {
        background-color: transparent !important;  /* Nền trong suốt */
        color: #000000 !important;  /* Màu chữ đen */
    }

    /* Đổi màu tiêu đề trong sidebar */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        color: #000000 !important;  /* Màu chữ đen cho tiêu đề */
    }

    /* Đổi màu các item trong sidebar */
    [data-testid="stSidebarNav"] ul li a {
        color: #000000 !important;  /* Màu chữ đen cho các item */
        font-size: 1.1em;  /* Tăng kích thước chữ cho dễ đọc */
        padding: 10px;
    }

    /* Màu khi hover (di chuột vào) */
    [data-testid="stSidebarNav"] ul li a:hover {
        background-color: #D1D5DB;  /* Màu nền khi hover */
        color: #000000;  /* Màu chữ đen khi hover */
    }

    /* Thêm hiệu ứng cho các item trong sidebar */
    [data-testid="stSidebarNav"] ul li {
        border-radius: 5px;  /* Bo góc cho các item */
        transition: background-color 0.3s ease;  /* Hiệu ứng chuyển màu mượt mà */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("# Chương 3")
FRAME_WINDOW = st.image([])

chuong3_options = [
    "Negative",
    "Negative Color",
    "Logarit",
    "Power",
    "Piecewise Linear",
    "Histogram",
    "HistEqual",
    "HistEqualColor",
    "LocalHist",
    "HistStat",
    "Smooth Box",
    "Smooth Gauss",
    "Median Filter",
    "Create Impulse Noise",
    "Sharp"]

def show():
    st.subheader("Chương 3")

    # --- Sidebar ---
    selected_option = st.selectbox("Chọn chức năng:", chuong3_options)

    # --- Upload ảnh ---
    uploaded_file = st.file_uploader("Chọn ảnh", type=["jpg", "jpeg", "png","tif","bmp","webp"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, 1)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        st.session_state.imgin = img_gray
        st.session_state.imgin_color = img_bgr

    # --- Hiển thị ảnh gốc ---
    if "imgin" in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            st.image(st.session_state.imgin_color, caption="Ảnh gốc")

        # --- Nút xử lý ---
        if st.button("Xử lý"):
            imgin = st.session_state.imgin
            imgin_color = st.session_state.imgin_color
            imgout = None

            if selected_option == "Negative":
                imgout = c3.Negative(imgin)
            elif selected_option == "Negative Color":
                imgout = c3.NegativeColor(imgin_color)
            elif selected_option == "Logarit":
                imgout = c3.Logarit(imgin)
            elif selected_option == "Power":
                imgout = c3.Power(imgin) 
            elif selected_option == "Piecewise Linear":
                imgout = c3.PiececwiseLinear(imgin)
            elif selected_option == "Histogram":
                imgout = c3.Histogram(imgin)
            elif selected_option == "HistEqual":
                imgout = cv2.equalizeHist(imgin)
            elif selected_option == "HistEqualColor":
                imgout = c3.HistEqualColor(imgin_color)
            elif selected_option == "LocalHist":
                imgout = c3.LocalHist(imgin)
            elif selected_option == "HistStat":
                imgout = c3.HistStat(imgin)
            elif selected_option == "Smooth Box":
                imgout =cv2.boxFilter(imgin, cv2.CV_8UC1, (21, 21))
            elif selected_option == "Smooth Gauss":
                imgout = cv2.GaussianBlur(imgin, (43, 43), 7)
            elif selected_option == "Median Filter":
                imgout = cv2.medianBlur(imgin, 5)
            elif selected_option == "Create Impulse Noise":
                imgout = c3.CreateImpulseNoise(imgin)
            elif selected_option == "Sharp":
                imgout = c3.Sharp(imgin)

            # --- Hiển thị ảnh đã xử lý ---
            if imgout is not None:
                with col2:
                    st.image(imgout, caption="Ảnh đã xử lý", channels="GRAY")

if __name__ == "__main__" or True:
    show()
