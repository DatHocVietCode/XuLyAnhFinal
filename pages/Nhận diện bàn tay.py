import cv2
import joblib
import mediapipe as mp
import numpy as np
import streamlit as st

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
