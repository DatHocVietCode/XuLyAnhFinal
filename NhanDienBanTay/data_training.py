import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier  # Import Random Forest
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Đọc dữ liệu từ file CSV
data = pd.read_csv('NhanDienBanTay/hand_data.csv')

# Tách dữ liệu thành features và labels
X = data.drop('label', axis=1)
y = data['label']

# Chia dữ liệu thành tập train và test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Huấn luyện mô hình với Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)  # Random Forest với 100 cây
model.fit(X_train, y_train)

# Dự đoán trên tập test
y_pred = model.predict(X_test)

# Đánh giá mô hình
print('Accuracy:', accuracy_score(y_test, y_pred))
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Lưu mô hình đã huấn luyện
joblib.dump((model, scaler), 'NhanDienBanTay/hand_model.pkl')
print('Đã lưu mô hình vào hand_model.pkl')
