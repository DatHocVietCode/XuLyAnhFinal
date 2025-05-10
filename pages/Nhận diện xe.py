import math
import os as os
import tempfile

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from ultralytics import YOLO

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
st.title("Nhận dạng loại xe và đếm số xe theo thời gian")
if "show_video" not in st.session_state:
    st.session_state.show_video = False
# Khởi tạo session state để lưu tọa độ line và background image
if 'start_line' not in st.session_state:
    st.session_state.start_line = None
if 'end_line' not in st.session_state:
    st.session_state.end_line = None
if 'canvas_key' not in st.session_state:
    st.session_state.canvas_key = 0
if 'background_image' not in st.session_state:
    st.session_state.background_image = None

# --- Drag and drop video ---
st.subheader("📤 Chọn video để xử lý")
uploaded_file = st.file_uploader("Kéo thả hoặc chọn một file video (.mp4)", type=["mp4", "avi"], key="custom_video_uploader")
# --- Drag and drop image ---
st.subheader("📤 Chọn ảnh để xử lý")
uploaded_image = st.file_uploader("Kéo thả hoặc chọn một file ảnh (.jpg, .png)", type=["jpg", "png"], key="custom_image_uploader")

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_path)
model = YOLO(os.path.join(base_path, 'vehicles_counting-master/model2/dataset/runs/detect/train/weights/best.pt'))
# Lấy danh sách các lớp từ model đã train
CLASSES = model.names
print(CLASSES)
#VEHICLE_CLASSES = [k for k, v in CLASSES.items() if v in ["car", "motorbike", "bus", "truck"]]
VEHICLE_CLASSES = [k for k, v in CLASSES.items() if v == "Vehicle"]
# Thiết lập một số tham số
CONFIDENCE_SETTING = 0.7
MAX_DISTANCE = 120



def detections_yolo(image):
    results = model.predict(image)

    boxes = []
    class_ids = []
    confidences = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            if confidence > CONFIDENCE_SETTING and class_id in VEHICLE_CLASSES:
                print(f"Object: {CLASSES[class_id]} - Confidence: {confidence:.2f}")
                boxes.append([x1, y1, x2 - x1, y2 - y1])
                class_ids.append(class_id)
                confidences.append(confidence)

    return boxes, class_ids, confidences



def draw_prediction(classes, colors, img, class_id, confidence, x, y, width, height):
    """
    Draw bounding box and put classe text and confidence
    :param classes: name of object
    :param colors: color for object
    :param img: immage
    :param class_id: class_id of this object
    :param confidence: confidence
    :param x: top, left
    :param y: top, left
    :param width: width of bounding box
    :param height: height of bounding box
    :return: None
    """
    try:
        label = str(classes[class_id])
        color = colors[class_id]
        center_x = int(x + width / 2.0)
        center_y = int(y + height / 2.0)
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)

        cv2.rectangle(img, (x, y), (x + width, y + height), color, 1)
        cv2.circle(img, (center_x, center_y), 2, (0, 255, 0), -1)
        cv2.putText(img, label + ": {:0.2f}%".format(confidence * 100), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    except (Exception, cv2.error) as e:
        print("Can't draw prediction for class_id {}: {}".format(class_id, e))

def detect_vehicle(video_input, video_output, skip_frame=1):
    """
    Phát hiện phương tiện trong video và lưu kết quả vào video đầu ra.

    Args:
        video_input (str): Đường dẫn đến video đầu vào.
        video_output (str): Đường dẫn để lưu video sau khi xử lý.
        skip_frame (int): Số lượng frame bỏ qua giữa mỗi lần nhận diện (giúp tối ưu tốc độ).

    Returns:
        None
    """
    # Tạo màu sắc ngẫu nhiên cho từng class
    colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # Load video
    cap = cv2.VideoCapture(video_input)
    ret_val, frame = cap.read()
    width = frame.shape[1]
    height = frame.shape[0]

    # Định dạng video đầu ra
    video_format = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_output, video_format, 25, (width, height))

    # Danh sách các đối tượng đang theo dõi
    list_object = []

    # Tạo vùng hiển thị trên Streamlit
    frame_container = st.empty()

    number_frame = 0  # Biến đếm số frame

    while cap.isOpened():
        number_frame += 1
        ret_val, frame = cap.read()
        if frame is None:
            break

        # ✨ **Detect object mới mỗi skip_frame**
        if number_frame % skip_frame == 0:
            results = model.predict(frame)
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])

                    if confidence > CONFIDENCE_SETTING and class_id in VEHICLE_CLASSES:
                        box_width, box_height = x2 - x1, y2 - y1

                        # ✨ **Vẽ bounding box của phương tiện**
                        draw_prediction(CLASSES, colors, frame, class_id, confidence,
                                        x1, y1, box_width, box_height)

        # Hiển thị frame trên Streamlit
        frame_container.image(frame, channels='BGR')
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def detect_vehicle_from_image(image_input, image_output):
    """
    Phát hiện phương tiện trong ảnh và lưu kết quả vào ảnh đầu ra.

    Args:
        image_input (str): Đường dẫn đến ảnh đầu vào.
        image_output (str): Đường dẫn để lưu ảnh sau khi xử lý.

    Returns:
        None
    """
    # Tạo màu sắc ngẫu nhiên cho từng class
    colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # Đọc ảnh
    img = cv2.imread(image_input)

    # Dự đoán phương tiện
    results = model.predict(img)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            if confidence > CONFIDENCE_SETTING and class_id in VEHICLE_CLASSES:
                box_width, box_height = x2 - x1, y2 - y1

                # Vẽ bounding box của phương tiện
                draw_prediction(CLASSES, colors, img, class_id, confidence,
                                x1, y1, box_width, box_height)

    # Lưu ảnh kết quả
    cv2.imwrite(image_output, img)



# --- Mặc định chạy video highway.mp4 nếu chưa có upload ---
default_video = os.path.join(base_path, "vehicles_counting-master", "Vehicle_Detection_on_Highway_Traffic_Lanes.mp4")
st.subheader("🎞️ Video mặc định")
if st.button("▶ Xử lý video mặc định"):
    output_default = os.path.join(tempfile.gettempdir(), "default_output.avi")
    detect_vehicle(default_video, output_default)
    st.video(output_default)
    st.session_state.show_video = True
    
if uploaded_file is not None:
    # Đọc video
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        tfile.close()  # Close the file after writing
        video_path = tfile.name
    else:
        video_path = default_video

    
    # Lấy frame đầu tiên
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if ret:
        if st.button("🚗 Bắt đầu nhận dạng xe"):
            output_path = os.path.join(tempfile.gettempdir(), "output.avi")
            detect_vehicle(video_path, output_path)


# --- Upload ảnh và xử lý ---
if uploaded_image is not None:
    # Lưu ảnh tạm thời
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_image.read())
    tfile.close()  # Close the file after writing
    image_path = tfile.name

    # Hiển thị ảnh gốc lên Streamlit
    st.image(image_path, caption="Ảnh gốc", use_column_width=True)

    if st.button("🚗 Nhận dạng phương tiện trong ảnh"):
        output_image = os.path.join(tempfile.gettempdir(), "output_image.jpg")
        detect_vehicle_from_image(image_path, output_image)

        # Hiển thị ảnh đã xử lý
        st.image(output_image, caption="Ảnh đã xử lý", use_column_width=True)

