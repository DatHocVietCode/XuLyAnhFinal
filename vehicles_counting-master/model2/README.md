✅ Thông tin chung:
Số epoch: 100 epochs

Thời gian train: 4.303 giờ (~4 giờ 18 phút)

Thiết bị: CPU (11th Gen Intel Core i5-11400H, 2.70GHz)

Version: Ultralytics 8.3.119, Python 3.10.11, Torch 2.7.0

Model parameters:

Số lượng lớp: 72 layers

Tổng số tham số: 3,005,843

FLOPs: 8.1 GFLOPs

Optimizer đã được loại bỏ (stripped) khỏi các file:

last.pt (6.3MB)

best.pt (6.3MB)

📊 Kết quả đánh giá (Validation):
Metrics	Giá trị
Precision (P)	0.915
Recall (R)	0.938
mAP@0.5	0.968
mAP@0.5:0.95	0.737

Precision (P): 91.5% — Mức độ chính xác khi model dự đoán một object.

Recall (R): 93.8% — Mức độ phát hiện đầy đủ các object có mặt trong ảnh.

mAP@0.5: 96.8% — Mức độ chính xác trung bình tại ngưỡng IoU là 0.5.

mAP@0.5:0.95: 73.7% — Mức độ chính xác trung bình trên các ngưỡng IoU từ 0.5 đến 0.95.

🚀 Hiệu suất xử lý:
Thời gian xử lý trên mỗi ảnh:

Preprocess: 7.6ms

Inference: 159.2ms

Postprocess: 1.8ms

📂 Kết quả được lưu tại:
runs/detect/train

💡 Nhận xét:
Model hoạt động tốt, với mAP@0.5 đạt gần 97%, rất phù hợp cho các bài toán detection yêu cầu độ chính xác cao.

mAP@0.5:0.95 cũng khá tốt (73.7%), chứng tỏ mô hình có khả năng nhận diện tốt ngay cả với những vật thể khó.

Precision và Recall đều cao, mô hình không chỉ phát hiện chính xác mà còn ít bỏ sót object.

Thời gian inference (~159ms/ảnh) trên CPU là hợp lý, tuy nhiên có thể cải thiện hơn nếu chuyển sang GPU.