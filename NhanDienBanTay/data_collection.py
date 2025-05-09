import csv
import os
import time

import cv2
import mediapipe as mp

# Khởi tạo Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Cấu hình webcam
cap = cv2.VideoCapture(0)

# Tạo file CSV để lưu dữ liệu
file_path = 'NhanDienBanTay/hand_data.csv'
is_empty = not os.path.exists(file_path) or os.path.getsize(file_path) == 0

with open(file_path, mode='a', newline='') as file:
    writer = csv.writer(file)

    # Ghi header nếu file chưa có nội dung
    if is_empty:
        header = [f'x{i}' for i in range(1, 22)] + [f'y{i}' for i in range(1, 22)] + [f'z{i}' for i in range(1, 22)] + ['label']
        writer.writerow(header)

    while True:
        # Nhập tên nhãn và số lượng tay
        label_input = input("Nhập tên nhãn và số lượng tay (VD: '4 1' hoặc '9 2'), nhấn B để thoát: ")
        if label_input.lower() == 'b':
            print("Kết thúc phiên thu thập dữ liệu.")
            break

        # Tách label và số lượng tay
        try:
            label, num_hands = label_input.split()
            num_hands = int(num_hands)
        except ValueError:
            print("❌ Sai định dạng. Vui lòng nhập lại đúng format: <label> <số lượng tay>")
            continue

        print(f"Bắt đầu thu thập dữ liệu cho nhãn: {label} với số lượng tay: {num_hands} trong 5 giây...")

        start_time = time.time()
        with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Không thể mở webcam.")
                    break

                image = cv2.flip(image, 1)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)

                # Vẽ bàn tay và thu thập tọa độ
                if results.multi_hand_landmarks:
                    if len(results.multi_hand_landmarks) != num_hands:
                        print(f"❌ Phát hiện {len(results.multi_hand_landmarks)} tay, nhưng cần {num_hands}. Bỏ qua frame này.")
                        continue

                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                        # Lấy tọa độ từng điểm
                        landmarks = []
                        for landmark in hand_landmarks.landmark:
                            landmarks.extend([landmark.x, landmark.y, landmark.z])

                        # ✅ Đảm bảo chỉ ghi nếu đủ 63 điểm (21 * 3)
                        if len(landmarks) == 63:
                            landmarks.append(label)
                            writer.writerow(landmarks)
                        else:
                            print("Không đủ điểm landmark. Bỏ qua frame này.")

                # Hiển thị hình ảnh
                cv2.imshow('Hand Data Collection', image)

                if time.time() - start_time > 10:
                    print(f"Đã kết thúc thu thập dữ liệu cho nhãn: {label}")
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Kết thúc phiên thu thập dữ liệu.")
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

cap.release()
cv2.destroyAllWindows()
print("Đã lưu dữ liệu vào NhanDienBanTay/hand_data.csv")
