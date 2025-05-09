import cv2
import joblib
import mediapipe as mp
import numpy as np
import streamlit as st

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
# Khởi tạo Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Cấu hình Streamlit
st.title("Hand Sign Recognition with Streamlit")
st.write("Bật webcam để nhận diện bàn tay theo thời gian thực.")

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

# Thiết lập cửa sổ để stream hình ảnh
frame_window = st.image([])
prediction_text = st.empty()

# Tải mô hình đã huấn luyện bằng joblib
model_path = 'NhanDienBanTay/hand_model.pkl'
try:
    # Đọc mô hình và các đối tượng đã lưu
    model, scaler = joblib.load(model_path)  # Giải nén 3 đối tượng
    st.success("Model loaded successfully!")
except FileNotFoundError:
    st.error("Không tìm thấy model.pkl. Vui lòng kiểm tra lại đường dẫn!")
    cap.release()
    cv2.destroyAllWindows()
    st.stop()

# Mediapipe hands
with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            st.error("Không thể mở webcam. Vui lòng kiểm tra lại!")
            break

        # Xử lý hình ảnh
        image = cv2.flip(image, 1)  # Lật ngược hình ảnh cho giống gương
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        # Vẽ khung bàn tay và lấy tọa độ
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Thu thập tọa độ bàn tay
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.extend([landmark.x, landmark.y, landmark.z])
                
                # Chuyển đổi sang numpy array để predict
                landmarks = np.array(landmarks).reshape(1, -1)
                
                # Kiểm tra số lượng feature cho khớp với scaler
                if landmarks.shape[1] == scaler.mean_.shape[0]:
                    landmarks = scaler.transform(landmarks)
                    # Dự đoán
                    try:
                        prediction = model.predict(landmarks)
                        probabilities = model.predict_proba(landmarks)  # Lấy xác suất dự đoán
                        confidence = np.max(probabilities) * 100       # Lấy độ chính xác cao nhất
                        label = prediction[0]
                        
                        # Hiển thị kết quả
                        prediction_text.text(f"Dự đoán: {label} (Độ chính xác: {confidence:.2f}%)")
                        cv2.putText(image, f'Prediction: {label} ({confidence:.2f}%)', 
                                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    except Exception as e:
                        st.error(f"Lỗi dự đoán: {e}")
                else:
                    st.warning("Kích thước vector không khớp với mô hình đã huấn luyện!")

        # Hiển thị lên Streamlit
        frame_window.image(image, channels='BGR')

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
