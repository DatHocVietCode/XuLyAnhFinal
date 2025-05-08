import argparse
import os

import cv2 as cv2
import joblib
import numpy as np
import streamlit as st

st.set_page_config(page_title="Nhận diện khuôn mặt")


st.markdown("# Nhận diện khuôn mặt")
FRAME_WINDOW = st.image([])
current_file_dir = os.path.dirname(os.path.abspath(__file__))

def str2bool(v):
    if v.lower() in ['on', 'yes', 'true', 'y', 't']:
        return True
    elif v.lower() in ['off', 'no', 'false', 'n', 'f']:
        return False
    else:
        raise NotImplementedError

parser = argparse.ArgumentParser()
parser.add_argument('--image1', '-i1', type=str, help='Path to the input image1. Omit for detecting on default camera.')
parser.add_argument('--image2', '-i2', type=str, help='Path to the input image2. When image1 and image2 parameters given then the program try to find a face on both images and runs face recognition algorithm.')
parser.add_argument('--video', '-v', type=str, help='Path to the input video.')
parser.add_argument('--scale', '-sc', type=float, default=1.0, help='Scale factor used to resize input video frames.')
parser.add_argument('--face_detection_model', '-fd', type=str, default='../model/face_detection_yunet_2023mar.onnx', help='Path to the face detection model. Download the model at https://github.com/opencv/opencv_zoo/tree/master/models/face_detection_yunet')
parser.add_argument('--face_recognition_model', '-fr', type=str, default='../model/face_recognition_sface_2021dec.onnx', help='Path to the face recognition model. Download the model at https://github.com/opencv/opencv_zoo/tree/master/models/face_recognition_sface')
parser.add_argument('--score_threshold', type=float, default=0.9, help='Filtering out faces of score < score_threshold.')
parser.add_argument('--nms_threshold', type=float, default=0.3, help='Suppress bounding boxes of iou >= nms_threshold.')
parser.add_argument('--top_k', type=int, default=5000, help='Keep top_k bounding boxes before NMS.')
parser.add_argument('--save', '-s', type=str2bool, default=False, help='Set true to save results. This flag is invalid when using camera.')
args = parser.parse_args()

svc = joblib.load(os.path.abspath(os.path.join(current_file_dir, "../NhanDangKhuonMat_onnx_Streamlit/model/svc.pkl")))
mydict = {
    0: "Dan",
    1: "Dat",
    2: "Son",
    3: "Tan",
    4: "Tri"
}

def visualize(input, faces, fps, results, thickness=2):
    if faces[1] is not None:
        for idx, face in enumerate(faces[1]):
            print('Face {}, top-left coordinates: ({:.0f}, {:.0f}), box width: {:.0f}, box height {:.0f}, score: {:.2f}'.format(idx, face[0], face[1], face[2], face[3], face[-1]))

            coords = face[:-1].astype(np.int32)
            # Hiển thị tên cho từng khuôn mặt
            if idx < len(results):
                cv2.putText(input, results[idx], (coords[0], coords[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(input, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), thickness)
            cv2.circle(input, (coords[4], coords[5]), 2, (255, 0, 0), thickness)
            cv2.circle(input, (coords[6], coords[7]), 2, (0, 0, 255), thickness)
            cv2.circle(input, (coords[8], coords[9]), 2, (0, 255, 0), thickness)
            cv2.circle(input, (coords[10], coords[11]), 2, (255, 0, 255), thickness)
            cv2.circle(input, (coords[12], coords[13]), 2, (0, 255, 255), thickness)
    cv2.putText(input, 'FPS: {:.2f}'.format(fps), (1, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


if __name__ == '__main__':
    # CHUẨN HÓA đường dẫn tuyệt đối
    face_detection_model_path = os.path.abspath(os.path.join(current_file_dir, "../NhanDangKhuonMat_onnx_Streamlit/model/face_detection_yunet_2023mar.onnx"))
    face_recognition_model_path = os.path.abspath(os.path.join(current_file_dir, "../NhanDangKhuonMat_onnx_Streamlit/model/face_recognition_sface_2021dec.onnx"))

    detector = cv2.FaceDetectorYN.create(
        face_detection_model_path,
        "",
        (320, 320),
        args.score_threshold,
        args.nms_threshold,
        args.top_k
    ) 
    recognizer = cv2.FaceRecognizerSF.create(
        face_recognition_model_path, ""
    )

    tm = cv2.TickMeter()

    cap = cv2.VideoCapture(0)
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    detector.setInputSize([frameWidth, frameHeight])

    dem = 0
    warmup_frames = 60
    FRAME_WINDOW = st.image([])
    result = "Unknown"  # Khởi tạo giá trị mặc định
    while True:
        hasFrame, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not hasFrame:
            print('No frames grabbed!')
            break

        # Inference
        tm.start()
        faces = detector.detect(frame) # faces is a tuple
        tm.stop()
        
        results = []  # Danh sách lưu kết quả nhận dạng cho từng khuôn mặt
        if faces[1] is not None:
            for face_info in faces[1]:
                face_align = recognizer.alignCrop(frame, face_info)
                face_feature = recognizer.feature(face_align)
                test_predict = svc.predict(face_feature)
                results.append(mydict[test_predict[0]])

        # Draw results on the input image
        visualize(frame, faces, tm.getFPS(), results)

        # Visualize results
        FRAME_WINDOW.image(frame, channels='BGR')
    cv2.destroyAllWindows()
