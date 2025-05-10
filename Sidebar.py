import streamlit as st

# =======================
# 🎨 CSS cho Sidebar
# =======================
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #1F2937;
        color: white;
    }
    [data-testid="stSidebar"] h2 {
        color: #60A5FA;
    }
    .nav-item {
        padding: 10px;
        margin-bottom: 5px;
        background-color: #374151;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .nav-item:hover {
        background-color: #4B5563;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =======================
# 📂 Menu Sidebar
# =======================
with st.sidebar:
    st.header("📌 Điều hướng")
    
    pages = {
        "🏠 Trang chủ": "home",
        "✋ Chương 3": "chapter3",
        "✋ Chương 4": "chapter4",
        "✋ Chương 9": "chapter9",
        "😊 Nhận diện khuôn mặt": "face_detection",
        "🚗 Nhận diện xe": "car_detection",
        "🚦 Nhận diện biển báo": "traffic_sign_detection",
        "🀄 Nhận diện cờ tướng": "chinese_chess_detection",
        "🍎 Phát hiện trái cây": "fruit_detection",
        "✋ Nhận diện cử chỉ bàn tay": "hand_gesture_detection"
    }
    
    selected_page = st.selectbox("Chọn trang:", list(pages.keys()))

    if st.button("Chuyển trang"):
        st.experimental_set_query_params(page=pages[selected_page])

def render_sidebar():
    st.sidebar.header("📌 Điều hướng")
    
    pages = {
        "🏠 Trang chủ": "home",
        "✋ Chương 3": "chapter3",
        "✋ Chương 4": "chapter4",
        "✋ Chương 9": "chapter9",
        "😊 Nhận diện khuôn mặt": "face_detection",
        "🚗 Nhận diện xe": "car_detection",
        "🚦 Nhận diện biển báo": "traffic_sign_detection",
        "✋ Nhận diện bàn tay": "hand_gesture_detection",
        "🀄 Nhận diện cờ tướng": "chinese_chess_detection",
        "🍎 Phát hiện trái cây": "fruit_detection"
    }

    choice = st.sidebar.radio("Chọn trang:", list(pages.keys()))

    # Lưu lựa chọn vào query params để chuyển trang
    st.experimental_set_query_params(page=pages[choice])