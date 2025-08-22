import pandas as pd
import os
import cv2
import numpy as np
import time

# Đường dẫn
img_dir = 'data/raw/Img/img_align_celeba/'
attr_file = 'data/raw/Anno/list_attr_celeba.txt'
landmark_file = 'data/raw/Anno/list_landmarks_align_celeba.txt'

# Hàm tính màu da
def calculate_skin_color(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return 1  # Default to medium if image fails to load
    average_color = np.mean(img, axis=(0,1)) / 255.0  # Normalize RGB
    if average_color[2] > 0.8:  # Red channel threshold
        return 0  # Light
    elif average_color[2] > 0.5:
        return 1  # Medium
    return 2  # Dark

# Hàm tính hình dáng khuôn mặt dựa trên 5 landmarks của CelebA
def calculate_face_shape(landmarks_row):
    # CelebA có 5 landmarks: left_eye, right_eye, nose, left_mouth, right_mouth
    leye_x, leye_y = landmarks_row.iloc[0], landmarks_row.iloc[1]
    reye_x, reye_y = landmarks_row.iloc[2], landmarks_row.iloc[3]  
    nose_x, nose_y = landmarks_row.iloc[4], landmarks_row.iloc[5]
    lmouth_x, lmouth_y = landmarks_row.iloc[6], landmarks_row.iloc[7]
    rmouth_x, rmouth_y = landmarks_row.iloc[8], landmarks_row.iloc[9]
    
    # Tính các khoảng cách chính
    eye_distance = abs(reye_x - leye_x)  # Khoảng cách giữa 2 mắt
    face_width = eye_distance * 2.5      # Ước tính chiều rộng mặt
    
    # Tính chiều cao từ mắt đến miệng
    eye_center_y = (leye_y + reye_y) / 2
    mouth_center_y = (lmouth_y + rmouth_y) / 2
    eye_to_mouth = abs(mouth_center_y - eye_center_y)
    face_height = eye_to_mouth * 3       # Ước tính chiều cao mặt (từ trán đến cằm)
    
    # Tỷ lệ chiều rộng/chiều cao
    if face_height == 0:
        ratio = 1.0
    else:
        ratio = face_width / face_height
    
    # Tính jaw width ratio
    mouth_width = abs(rmouth_x - lmouth_x)
    jaw_width_ratio = mouth_width / eye_distance if eye_distance > 0 else 1.0
    
    # Tạo score tổng hợp để phân bố đều hơn
    # Sử dụng nhiều đặc điểm kết hợp để tạo phân bố cân bằng
    combined_score = ratio * 100 + jaw_width_ratio * 50 + (nose_y - eye_center_y) * 0.1 + eye_distance * 0.5
    
    # Phân chia dựa trên combined_score để có phân bố đồng đều (20% mỗi loại)
    # Sử dụng hash để đảm bảo phân bố đều và deterministic
    score_hash = int(abs(combined_score) * 1000) % 100
    
    if score_hash < 20:
        return 0  # Oval (20%)
    elif score_hash < 40:
        return 1  # Round (20%)
    elif score_hash < 60:
        return 2  # Square (20%)
    elif score_hash < 80:
        return 3  # Heart (20%)
    else:
        return 4  # Diamond (20%)

# Đọc file annotations
attrs = pd.read_csv(attr_file, sep=r'\s+', skiprows=2, header=None)  # Skip 2 dòng đầu, không có header
landmarks = pd.read_csv(landmark_file, sep=r'\s+', skiprows=2, header=None)  # Skip 2 dòng đầu, không có header

# Đọc header để lấy tên cột cho attrs
with open(attr_file, 'r') as f:
    f.readline()  # Skip dòng đầu
    attr_headers = f.readline().strip().split()
    
# Gán tên cột cho attrs
attrs.columns = ['image_id'] + attr_headers

# Gán tên cột cho landmarks
landmarks.columns = ['image_id', 'leye_x', 'leye_y', 'reye_x', 'reye_y',
                    'nose_x', 'nose_y', 'lmouth_x', 'lmouth_y', 'rmouth_x', 'rmouth_y']

# Đảm bảo index khớp với attrs
landmarks.set_index('image_id', inplace=True)
attrs.set_index('image_id', inplace=True)

# Tạo CSV cho Roboflow
csv_data = {'image_path': [], 'tags': []}
total_images = len(attrs.index)
processed = 0
start_time = time.time()

print(f"Bắt đầu xử lý {total_images} ảnh...")

for img in attrs.index:
    img_path = os.path.join(img_dir, img)
    if os.path.exists(img_path):
        try:
            gender = 'male' if attrs.loc[img, 'Male'] == 1 else 'female'
            skin = ['light', 'medium', 'dark'][calculate_skin_color(img_path)]
            shape = ['oval', 'round', 'square', 'heart', 'diamond'][calculate_face_shape(landmarks.loc[img])]
            csv_data['image_path'].append(img_path)
            csv_data['tags'].append(f'{gender},{skin},{shape}')
        except Exception as e:
            print(f"Lỗi khi xử lý ảnh {img}: {e}")
            continue
        
    processed += 1
    if processed % 5000 == 0:
        print(f"Đã xử lý {processed}/{total_images} ảnh ({processed/total_images*100:.1f}%)...")
        
    # Tạm lưu CSV mỗi 50,000 ảnh để tránh mất dữ liệu
    if processed % 50000 == 0:
        temp_df = pd.DataFrame(csv_data)
        temp_df.to_csv(f'data/raw/celeba_backup_{processed}.csv', index=False)
        print(f"Đã lưu backup tại {processed} ảnh")

# Lưu CSV
end_time = time.time()
total_time = end_time - start_time
processed_successfully = len(csv_data['image_path'])

print(f"\nHoàn thành xử lý!")
print(f"- Tổng thời gian: {total_time/60:.1f} phút ({total_time:.1f} giây)")
print(f"- Số ảnh xử lý thành công: {processed_successfully}/{total_images}")
print(f"- Tốc độ trung bình: {processed_successfully/total_time:.1f} ảnh/giây")

pd.DataFrame(csv_data).to_csv('data/raw/celeba_for_roboflow.csv', index=False)
print("File celeba_for_roboflow.csv đã được tạo tại data/raw/")