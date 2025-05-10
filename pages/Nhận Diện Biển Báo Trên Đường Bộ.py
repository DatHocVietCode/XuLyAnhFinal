import os

import cv2
import numpy as np
import streamlit as st
from PIL import Image

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
# Trang trí tiêu đề
st.markdown("""
    <h1 style='text-align: center; color: #2E86C1;'>🚦 Nhận dạng biển báo đường bộ 🚦</h1>
""", unsafe_allow_html=True)

# Mô tả và hướng dẫn
st.markdown("""
<div style='text-align: center; font-size:18px;'>
Ứng dụng sử dụng trí tuệ nhân tạo để nhận diện các loại biển báo giao thông trên đường bộ Việt Nam.<br>
<b>Hướng dẫn:</b> <br>
1. Nhấn <b>Browse files</b> để tải lên ảnh biển báo.<br>
2. Nhấn <b>Predict</b> để xem kết quả nhận diện.<br>
</div>
---
""", unsafe_allow_html=True)

try:
    if st.session_state["LoadModel"] == True:
        print('Model is loaded')
except:
    st.session_state["LoadModel"] = True
    st.session_state["Net"] = cv2.dnn.readNet("NhanDienBienBao/road_sign_detection_model.onnx")
    print(st.session_state["LoadModel"])
    print('Load model lần đầu')
     
filename_classes = 'NhanDienBienBao/road_signs_classes.txt'
mywidth  = 640
myheight = 640
postprocessing = 'yolov8'
background_label_id = -1
backend = 0
target = 0

# Load names of classes
classes = None
if filename_classes:
    with open(filename_classes, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

st.session_state["Net"].setPreferableBackend(0)
st.session_state["Net"].setPreferableTarget(0)
outNames = st.session_state["Net"].getUnconnectedOutLayersNames()

confThreshold = 0.5
nmsThreshold = 0.4
scale = 0.00392
mean = [0, 0, 0]

def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Danh sách kết quả nhận diện
    detected_objects = []

    def drawPred(classId, conf, left, top, right, bottom):
        # Vẽ khung bao quanh đối tượng
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Tạo nhãn với độ chính xác
        label = '%.2f' % conf
        if classes:
            assert(classId < len(classes))
            label = f'{classes[classId]}: {label}'

        # Kích thước của label
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])

        # Vẽ nhãn lên ảnh
        cv2.rectangle(frame, (left, top - labelSize[1]), 
                      (left + labelSize[0], top + baseLine), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        # Thêm đối tượng nhận diện vào danh sách kết quả
        detected_objects.append((classes[classId], conf, (left, top, right - left, bottom - top)))

    # Lấy tên lớp và lớp cuối cùng
    layerNames = st.session_state["Net"].getLayerNames()
    lastLayerId = st.session_state["Net"].getLayerId(layerNames[-1])
    lastLayer = st.session_state["Net"].getLayer(lastLayerId)

    classIds = []
    confidences = []
    boxes = []

    if lastLayer.type == 'Region' or postprocessing == 'yolov8':
        if postprocessing == 'yolov8':
            box_scale_w = frameWidth / mywidth
            box_scale_h = frameHeight / myheight
        else:
            box_scale_w = frameWidth
            box_scale_h = frameHeight

        for out in outs:
            if postprocessing == 'yolov8':
                out = out[0].transpose(1, 0)

            for detection in out:
                scores = detection[4:]
                if background_label_id >= 0:
                    scores = np.delete(scores, background_label_id)
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThreshold:
                    center_x = int(detection[0] * box_scale_w)
                    center_y = int(detection[1] * box_scale_h)
                    width = int(detection[2] * box_scale_w)
                    height = int(detection[3] * box_scale_h)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
    else:
        print('Unknown output layer type: ' + lastLayer.type)
        exit()

    # Non-Maximum Suppression (NMS) để loại bỏ các bounding box bị trùng
    if len(outNames) > 1 or (lastLayer.type == 'Region' or postprocessing == 'yolov8') and 0 != cv2.dnn.DNN_BACKEND_OPENCV:
        indices = []
        classIds = np.array(classIds)
        boxes = np.array(boxes)
        confidences = np.array(confidences)
        unique_classes = set(classIds)
        for cl in unique_classes:
            class_indices = np.where(classIds == cl)[0]
            conf = confidences[class_indices]
            box = boxes[class_indices].tolist()
            nms_indices = cv2.dnn.NMSBoxes(box, conf, confThreshold, nmsThreshold)
            indices.extend(class_indices[nms_indices])
    else:
        indices = np.arange(0, len(classIds))

    # Vẽ các bounding box và lưu vào danh sách kết quả
    for i in indices:
        box = boxes[i]
        left, top, width, height = box
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)

    # Trả về danh sách các đối tượng nhận diện
    return detected_objects


img_file_buffer = st.file_uploader("**Upload ảnh biển báo**", type=["bmp", "png", "jpg", "jpeg"], help="Chọn ảnh biển báo giao thông để nhận diện.")
col1, col2 = st.columns([1,1])

if img_file_buffer is not None:
    image = Image.open(img_file_buffer) 
    # Chuyển sang định dạng OpenCV để xử lý
    frame = np.array(image)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Ảnh gốc tải lên", use_column_width=True)
        
    if st.button('🔍 Predict'):
        with st.spinner('⏳ Đang nhận diện biển báo...'):
            if frame is not None:
                frameHeight = frame.shape[0]
                frameWidth = frame.shape[1]

                # Khởi tạo blob cho mạng nơ-ron
                inpWidth = mywidth if mywidth else frameWidth
                inpHeight = myheight if myheight else frameHeight
                blob = cv2.dnn.blobFromImage(frame, size=(inpWidth, inpHeight), swapRB=True, ddepth=cv2.CV_8U)

                # Chạy mô hình
                st.session_state["Net"].setInput(blob, scalefactor=scale, mean=mean)
                if st.session_state["Net"].getLayer(0).outputNameToIndex('im_info') != -1:
                    frame = cv2.resize(frame, (inpWidth, inpHeight))
                    st.session_state["Net"].setInput(np.array([[inpHeight, inpWidth, 1.6]], dtype=np.float32), 'im_info')

                outs = st.session_state["Net"].forward(outNames)

                # **Xử lý kết quả sau khi dự đoán**
                detected_objects = postprocess(frame, outs)

                # Chuyển ảnh lại về RGB để hiển thị với PIL
                color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                pil_image = Image.fromarray(color_coverted) 
                
                with col2:
                    st.image(pil_image, caption="Kết quả nhận dạng", use_column_width=True)
                    st.success('✅ Đã nhận diện xong!')

                # **Hiển thị thông tin nhận diện**
                if detected_objects:
                    st.markdown("### Kết quả nhận diện:")
                    for obj in detected_objects:
                        label, confidence, (x, y, w, h) = obj
                        st.write(f"- **Biển báo**: {label} | **Độ chính xác**: {confidence * 100:.2f}% | **Vị trí**: ({x}, {y}, {w}, {h})")
                else:
                    st.warning("⚠️ Không tìm thấy biển báo nào!")


