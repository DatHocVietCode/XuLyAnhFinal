import random
import time

import cv2
import joblib
import mediapipe as mp
import numpy as np
import streamlit as st

# ============ Cấu hình giao diện Streamlit ============
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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("✋ Kéo - Búa - Bao ✊")
st.write("👆 Bật webcam và chơi game trực tiếp với máy tính!")

# ============ Khởi tạo Mediapipe ============
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# ============ Khởi tạo webcam ============
cap = cv2.VideoCapture(0)
frame_window = st.image([])
result_text = st.empty()
user_choice_text = st.empty()
computer_choice_text = st.empty()
score_text = st.empty()

# ============ Tải mô hình nhận diện ============
model_path = 'NhanDienBanTay/hand_model.pkl'
try:
    model, scaler = joblib.load(model_path)
    st.success("🎉 Model loaded successfully!")
except FileNotFoundError:
    st.error("❌ Không tìm thấy hand_model.pkl. Vui lòng kiểm tra lại đường dẫn!")
    cap.release()
    cv2.destroyAllWindows()
    st.stop()

# ============ Lựa chọn ngẫu nhiên của máy ============
choices = ['keo', 'bua', 'bao']

# ============ Biến điều khiển ============
pause_prediction = False
last_update_time = 0
user_score, computer_score, draw_score = 0, 0, 0
user_choice, computer_choice = None, None
confirmed_choice = None
start_confirmation_time = None

# ============ Hàm xác định kết quả ============
def get_winner(user, computer):
    global user_score, computer_score, draw_score
    if user == computer:
        draw_score += 1
        return "Draw!"
    elif (user == 'keo' and computer == 'bao') or (user == 'bua' and computer == 'keo') or (user == 'bao' and computer == 'bua'):
        user_score += 1
        return "You win!"
    else:
        computer_score += 1
        return "You loose!"

# ============ Vòng lặp chơi game ============
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            st.error("❌Can't open camera")
            break
        
        # Xử lý hình ảnh
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if not pause_prediction:
            # Dự đoán bàn tay
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Lấy tọa độ bàn tay
                    landmarks = [coord for landmark in hand_landmarks.landmark for coord in (landmark.x, landmark.y, landmark.z)]
                    landmarks = np.array(landmarks).reshape(1, -1)

                    if landmarks.shape[1] == scaler.mean_.shape[0]:
                        landmarks = scaler.transform(landmarks)
                        try:
                            prediction = model.predict(landmarks)
                            current_choice = prediction[0]
                            
                            # Kiểm tra lựa chọn ổn định sau 1.5 giây
                            if confirmed_choice is None or current_choice != confirmed_choice:
                                confirmed_choice = current_choice
                                start_confirmation_time = time.time()
                            elif time.time() - start_confirmation_time >= 1.5:
                                user_choice = confirmed_choice
                        except Exception as e:
                            st.error(f"Lỗi dự đoán: {e}")
            
            # Máy tính chọn ngẫu nhiên và xử lý sau khi xác nhận xong
            if user_choice:
                computer_choice = random.choice(choices)

                # Hiển thị thông tin lên Streamlit
                user_choice_text.text(f"✋ Bạn chọn: **{user_choice}**")
                computer_choice_text.text(f"💻 Máy chọn: **{computer_choice}**")
                result_text.text(get_winner(user_choice, computer_choice))
                
                # Cập nhật điểm số
                score_text.text(f"🔴 Bạn: {user_score} | 💻 Máy: {computer_score} | 🤝 Hòa: {draw_score}")

                # Tạm dừng dự đoán 5 giây
                pause_prediction = True
                last_update_time = time.time()
        
         # Nếu đang tạm dừng thì vẫn hiển thị kết quả lên webcam
        if pause_prediction:
            # Hiển thị lựa chọn của bạn
            cv2.putText(image, f"Ban: {user_choice}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Hiển thị lựa chọn của máy
            cv2.putText(image, f"May: {computer_choice}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Hiển thị kết quả (lùi xuống một dòng nữa để không bị đè)
            cv2.putText(image, get_winner(user_choice, computer_choice), (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        # Kiểm tra nếu đã qua 5 giây thì tiếp tục nhận diện
        if pause_prediction and (time.time() - last_update_time) > 5:
            pause_prediction = False
            result_text.text("")
            user_choice_text.text("")
            computer_choice_text.text("")
            user_choice, computer_choice = None, None
            confirmed_choice = None

        # Cập nhật frame lên Streamlit
        frame_window.image(image, channels='BGR')

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
