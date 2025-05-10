import streamlit as st

# =======================
# 🚀 Cấu hình trang
# =======================
st.set_page_config(
    page_title="Đồ án cuối kỳ",
    page_icon="📘",
    layout="centered"
)
# =======================
# 🎨 Thêm background
# =======================
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://moewalls.com/wp-content/uploads/2024/11/cat-floating-on-the-water-thumb-728x410.jpg");
        background-size: cover;
        background-position: center;
        color: white;
    }
    
    .title {
        color: ;
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
        color: black;  /* Màu chữ đen khi hover */
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
# =======================
# 🌟 Hiển thị nội dung
# =======================
st.markdown('<div class="title">Đồ án cuối kỳ</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Xử lý ảnh số</div>', unsafe_allow_html=True)

# -----------------------
# 🔹 Sản phẩm
# -----------------------
st.markdown('<div class="section-title">📌 Sản phẩm</div>', unsafe_allow_html=True)
st.markdown('<div class="info">Project cuối kỳ cho môn học xử lý ảnh số thuộc Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM.</div>', unsafe_allow_html=True)
st.markdown('''<ul class="info">
        <li>📚 <strong>Chương 3:</strong> Xử lý ảnh</li>
        <li>📚 <strong>Chương 4:</strong> Xử lý ảnh</li>
        <li>📚 <strong>Chương 9:</strong> Xử lý ảnh</li>
        <li>🤖 <strong>Nhận dạng khuôn mặt</strong></li>
        <li>🚗 <strong>Nhận dạng loại xe</strong></li>
        <li>🚦 <strong>Nhận diện biển báo</strong></li>
        <li>✋ <strong>Nhận diện bàn tay</strong></li>
        <li>♟️ <strong>Nhận diện cờ tướng</strong></li>
        <li>🍎 <strong>Phát hiện trái cây</strong></li>
    </ul>''', unsafe_allow_html=True)
# -----------------------
# 🔹 Thông tin sinh viên
# -----------------------
st.markdown('<div class="section-title">👨‍🎓 Thông tin sinh viên thực hiện</div>', unsafe_allow_html=True)
st.markdown('''<ul class="info">
    <li>📝 Họ tên: Võ Phan Tấn Đạt</li> 
    <li>🆔 MSSV: 22110309</li>
</ul>''', unsafe_allow_html=True)
