import pandas as pd

csv_path = 'NhanDienBanTay/hand_data.csv'

# Đọc file CSV
try:
    df = pd.read_csv(csv_path)
except pd.errors.ParserError:
    print("File CSV bị lỗi, không thể đọc được.")
    exit()

# Xóa các dòng header trùng lặp (nếu có dòng nào chứa 'x1', 'y1', 'z1' ở đầu)
header_row = df.columns.tolist()
df = df[~df.eq(header_row).all(axis=1)]

# Ghi lại vào file CSV, không ghi thêm index
df.to_csv(csv_path, index=False)

print("Đã xóa các dòng header trùng lặp thành công!")
