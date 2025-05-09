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
        background-image: url("https://c4.wallpaperflare.com/wallpaper/586/603/742/minimalism-4k-for-mac-desktop-wallpaper-preview.jpg");
        background-size: cover;
        background-position: center;
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

# =======================
# 🌟 Hiển thị nội dung
# =======================
st.markdown('<div class="title">Đồ án cuối kỳ</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Xử lý ảnh số - DIPR430685_23_2_03</div>', unsafe_allow_html=True)

# -----------------------
# 🔹 Sản phẩm
# -----------------------
st.markdown('<div class="section-title">📌 Sản phẩm</div>', unsafe_allow_html=True)
st.markdown('<div class="info">Project cuối kỳ cho môn học xử lý ảnh số thuộc Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM.</div>', unsafe_allow_html=True)

st.markdown('''<ul class="info">
    <li>📖 Chương 3: Xử lý ảnh</li>
    <li>📖 Chương 4: Xử lý ảnh</li>
    <li>📖 Chương 9: Xử lý ảnh</li>
    <li>📖 Nhận dạng khuôn mặt</li>
    <li>📖 Nhận dạng loại xe</li>
    <li>📖 Nhận diện biển báo</li>
</ul>''', unsafe_allow_html=True)

# -----------------------
# 🔹 Thông tin sinh viên
# -----------------------
st.markdown('<div class="section-title">👨‍🎓 Thông tin sinh viên thực hiện</div>', unsafe_allow_html=True)
st.markdown('''<ul class="info">
    <li>📝 Họ tên: Võ Phan Tấn Đạt</li>
    <li>📝 Họ tên: Võ Phan Tấn Đạt</li>
    <li>🆔 MSSV: 22110309</li>
</ul>''', unsafe_allow_html=True)

st.markdown('<div class="section-title">🌐 Liên hệ</div>', unsafe_allow_html=True)
st.markdown('''<ul class="info contact">
    <li>🔗 <a href="https://github.com/DatHocVietCode" target="_blank">GitHub: DatHocVietCode</a></li>
    <li>🔗 <a href="mailto:td13052004@gmail.com">Email: td13052004@gmail.com</a></li>
    <li>🔗 <a href="https://www.facebook.com/vo.phan.tan.at/" target="_blank">Facebook: Võ Phan Tấn Đạt</a></li>
</ul>''', unsafe_allow_html=True)
