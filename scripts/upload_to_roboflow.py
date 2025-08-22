import pandas as pd
import os
from roboflow import Roboflow
import shutil
from tqdm import tqdm

# Cấu hình Roboflow
# Bạn cần lấy API key từ https://roboflow.com/settings/api
API_KEY = "YOUR_API_KEY_HERE"  # Thay bằng API key của bạn
WORKSPACE_ID = "YOUR_WORKSPACE"  # Thay bằng workspace của bạn
PROJECT_ID = "face-classification"  # Tên project

def setup_roboflow_project():
    """
    Thiết lập và upload dataset lên Roboflow cho Single-Label Gender Classification
    """
    
    print("🚀 Bắt đầu setup Roboflow project...")
    print("🎯 Single-Label Classification: Gender Detection (Female vs Male)")
    
    # Đọc dataset
    df = pd.read_csv('data/raw/celeba_for_roboflow.csv')
    print(f"📊 Dataset có {len(df)} ảnh")
    
    # Tạo thư mục tạm để organize dữ liệu theo format Roboflow Classification
    temp_dir = "temp_roboflow_gender"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    print("📁 Tạo cấu trúc thư mục cho Gender Classification...")
    
    # Tạo thư mục cho 2 classes: female và male
    os.makedirs(f"{temp_dir}/female", exist_ok=True)
    os.makedirs(f"{temp_dir}/male", exist_ok=True)
    
    print("🏷️  Classes: female, male")
    
    # Copy và organize ảnh theo gender
    print("📋 Organize ảnh theo gender...")
    
    copied_count = 0
    max_per_class = 3000  # Giới hạn để test trước (cân bằng dataset)
    class_counts = {"female": 0, "male": 0}
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing images"):
        gender = row['tags'].split(',')[0]  # Lấy gender (female/male)
        
        # Giới hạn số ảnh mỗi class để có dataset cân bằng
        if class_counts[gender] >= max_per_class:
            continue
            
        img_path = row['image_path']
        if os.path.exists(img_path):
            # Tạo tên file mới
            img_name = os.path.basename(img_path)
            dest_path = f"{temp_dir}/{gender}/{img_name}"
            
            try:
                shutil.copy2(img_path, dest_path)
                class_counts[gender] += 1
                copied_count += 1
            except Exception as e:
                print(f"❌ Lỗi copy {img_path}: {e}")
                continue
    
    print(f"✅ Đã copy {copied_count} ảnh cho Gender Classification")
    print(f"   Female: {class_counts['female']} ảnh ({class_counts['female']/copied_count*100:.1f}%)")
    print(f"   Male: {class_counts['male']} ảnh ({class_counts['male']/copied_count*100:.1f}%)")
    
    print(f"\n📁 Dataset structure:")
    print(f"   {temp_dir}/")
    print(f"   ├── female/ ({class_counts['female']} images)")
    print(f"   └── male/ ({class_counts['male']} images)")
    
    print("\n🔑 Bước tiếp theo:")
    print("1. Truy cập https://roboflow.com và tạo tài khoản")
    print("2. Create New Project > Classification > Single-Label")
    print("3. Project name: 'gender-classification'")
    print("4. Upload folder: temp_roboflow_gender/")
    print("5. Roboflow sẽ tự động detect 2 classes: female, male")
    
    return temp_dir

def upload_to_roboflow(temp_dir, api_key=None):
    """
    Upload dataset lên Roboflow (cần API key)
    """
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("❌ Cần API key để upload. Vui lòng:")
        print("1. Truy cập https://roboflow.com/settings/api") 
        print("2. Copy API key")
        print("3. Thay đổi API_KEY trong script")
        return
    
    try:
        # Khởi tạo Roboflow
        rf = Roboflow(api_key=api_key)
        
        # Tạo hoặc truy cập workspace
        workspace = rf.workspace(WORKSPACE_ID)
        
        # Upload dataset
        print("🚀 Bắt đầu upload dataset...")
        
        # Note: Roboflow classification upload cần được thực hiện qua web interface
        # hoặc sử dụng specific API calls
        print("📝 Để upload Classification dataset:")
        print("1. Vào https://roboflow.com/your-workspace/projects")
        print("2. Click 'Upload Data'")
        print("3. Chọn 'Folder Upload'")
        print(f"4. Upload thư mục: {temp_dir}/")
        print("5. Roboflow sẽ tự động detect classes từ folder structure")
        
    except Exception as e:
        print(f"❌ Lỗi kết nối Roboflow: {e}")
        print("Vui lòng kiểm tra API key và workspace ID")

if __name__ == "__main__":
    # Bước 1: Organize dữ liệu
    temp_dir = setup_roboflow_project()
    
    # Bước 2: Upload (tùy chọn, cần API key)
    # upload_to_roboflow(temp_dir, API_KEY)
    
    print(f"\n🎯 Dataset đã sẵn sàng trong thư mục: {temp_dir}/")
    print("📤 Bạn có thể upload manual hoặc sử dụng API")
