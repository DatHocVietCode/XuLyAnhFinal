import csv
import time

import cv2
import mediapipe as mp

# Khởi tạo Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Cấu hình webcam
cap = cv2.VideoCapture(0)

# Tạo file CSV để lưu dữ liệu
with open('NhanDienBanTay/hand_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    # Ghi header (x1, y1, z1, ..., x21, y21, z21, label)
    header = [f'x{i}' for i in range(1, 22)] + [f'y{i}' for i in range(1, 22)] + [f'z{i}' for i in range(1, 22)] + ['label']
    writer.writerow(header)

    while True:
        label = input("Nhập tên nhãn (label) cho bộ dữ liệu này (hoặc nhấn B để kết thúc): ")
        if label.lower() == 'b':
            print("Kết thúc phiên thu thập dữ liệu.")
            break

        # Bắt đầu thu thập dữ liệu trong 5 giây
        print(f"Bắt đầu thu thập dữ liệu cho nhãn: {label} trong 5 giây...")
        
        start_time = time.time()
        with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Không thể mở webcam.")
                    break

                # Lật ngược hình ảnh và chuyển sang RGB
                image = cv2.flip(image, 1)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)

                # Vẽ bàn tay và thu thập tọa độ
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                        # Lấy tọa độ từng điểm
                        landmarks = []
                        for landmark in hand_landmarks.landmark:
                            landmarks.extend([landmark.x, landmark.y, landmark.z])

                        # Ghi vào CSV
                        landmarks.append(label)
                        writer.writerow(landmarks)

                # Hiển thị hình ảnh
                cv2.imshow('Hand Data Collection', image)

                # Dừng sau 5 giây
                if time.time() - start_time > 10:
                    print(f"Đã kết thúc thu thập dữ liệu cho nhãn: {label}")
                    break

                # Bấm 'q' để thoát khẩn cấp
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Kết thúc phiên thu thập dữ liệu.")
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
print("Đã lưu dữ liệu vào NhanDienBanTay/hand_data.csv")
