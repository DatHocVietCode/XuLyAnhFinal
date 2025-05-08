lệnh train:
yolo task=detect mode=train data="D:/University/Nam3/2stSemester/XuLyAnh/22110309/vehicles_counting-master/model/dataset/data.yaml" model=yolov8n.pt epochs=100 imgsz=640

Mô Hình Xe Cộ - Đếm và Nhận Diện
Mô Tả Mô Hình
Mô hình này được huấn luyện để nhận diện và đếm các loại phương tiện giao thông, bao gồm xe ô tô, xe máy, xe buýt và xe tải. Mô hình sử dụng kiến trúc YOLOv5 với trọng số đã được huấn luyện trên bộ dữ liệu phương tiện giao thông.

Thông Số Mô Hình
Số lớp: 72 lớp

Tổng số tham số: 3,006,428 tham số

GFLOPs: 8.1 GFLOPs (Floating Point Operations Per Second)

Trọng số mô hình:

last.pt (trọng số mô hình cuối cùng)

best.pt (trọng số mô hình tốt nhất)

Kết Quả Đánh Giá
Tổng Quan:
mAP50 (mean Average Precision tại IoU=50%): 0.757

mAP50-95 (mean Average Precision qua các ngưỡng IoU từ 50% đến 95%): 0.538

Hiệu Suất Theo Các Lớp:
Car:

mAP50: 0.950

mAP50-95: 0.754

Hiệu suất cao trong việc nhận diện xe ô tô.

Motorbike:

mAP50: 0.944

mAP50-95: 0.672

Hiệu suất rất tốt trong việc nhận diện xe máy.

Bus:

mAP50: 0.397

mAP50-95: 0.170

Mô hình gặp khó khăn trong việc nhận diện xe buýt, cần cải tiến thêm.

Truck:

mAP50: 0.735

mAP50-95: 0.556

Hiệu suất nhận diện xe tải ổn, nhưng cần cải thiện ở mức độ chi tiết.

Thời Gian Xử Lý
Thời gian xử lý mỗi ảnh:

Preprocessing: 1.1ms

Inference: 54.7ms

Loss: 0ms

Postprocessing: 0.6ms

Đánh Giá Tổng Quan
Mô hình đã đạt được hiệu suất rất tốt trong việc nhận diện car và motorbike.

Kết quả đối với bus vẫn còn khá thấp và cần cải tiến thêm.

Có thể thử cải thiện mô hình bằng cách tăng cường dữ liệu hoặc sử dụng các kỹ thuật nâng cao khác để cải thiện mAP50-95 cho các lớp.

