"""
Alternative Python script để upload dataset lên Roboflow
Sử dụng khi CLI không hoạt động hoặc muốn control chi tiết hơn
"""

import os
import time
from tqdm import tqdm
from roboflow import Roboflow

# Configuration - ĐÃ CẬP NHẬT VỚI THÔNG TIN CỦA BẠN
API_KEY = "lde2hp1C5PxcfTaUwjox"  # Private API Key
WORKSPACE_ID = "faceshapedetect"  # Workspace ID
PROJECT_NAME = "gender-classification-uzvfc"  # Project ID

def upload_with_python_api():
    """
    Upload dataset sử dụng Python API
    """
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Vui lòng cập nhật API_KEY trong script")
        print("1. Truy cập https://roboflow.com/settings/api")
        print("2. Copy Private API Key")
        print("3. Thay thế API_KEY trong script")
        return
    
    if WORKSPACE_ID == "YOUR_WORKSPACE_ID":
        print("❌ Vui lòng cập nhật WORKSPACE_ID trong script")
        print("1. Tìm workspace ID trong URL: https://app.roboflow.com/{WORKSPACE_ID}/")
        print("2. Thay thế WORKSPACE_ID trong script")
        return
    
    print("🚀 Bắt đầu upload với Python API...")
    
    try:
        # Initialize Roboflow
        print("🔑 Đăng nhập Roboflow...")
        rf = Roboflow(api_key=API_KEY)
        
        # Get workspace and project
        workspace = rf.workspace(WORKSPACE_ID)
        project = workspace.project(PROJECT_NAME)
        
        print(f"✅ Kết nối thành công: {WORKSPACE_ID}/{PROJECT_NAME}")
        
        # Dataset path
        dataset_path = "roboflow_gender_dataset"
        if not os.path.exists(dataset_path):
            print(f"❌ Không tìm thấy dataset: {dataset_path}")
            print("Vui lòng chạy scripts/upload_cli.sh trước")
            return
        
        # Upload images từng class
        classes = ["female", "male"]
        
        for class_name in classes:
            class_path = os.path.join(dataset_path, class_name)
            if not os.path.exists(class_path):
                print(f"⚠️  Không tìm thấy class: {class_path}")
                continue
                
            images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"📤 Upload {len(images)} ảnh cho class '{class_name}'...")
            
            # Upload từng ảnh với progress bar
            for img_name in tqdm(images, desc=f"Uploading {class_name}"):
                img_path = os.path.join(class_path, img_name)
                
                try:
                    # Upload image với annotation
                    project.upload(
                        image_path=img_path,
                        annotation_name=class_name,  # Single-label classification
                        hosted=True  # Host on Roboflow
                    )
                    
                    # Rate limiting - tránh spam API
                    time.sleep(0.1)  # 100ms delay
                    
                except Exception as e:
                    print(f"❌ Lỗi upload {img_name}: {e}")
                    continue
        
        print("✅ Upload hoàn tất!")
        print("\n🎯 Bước tiếp theo:")
        print("1. Truy cập Roboflow project")
        print("2. Review uploaded images")
        print("3. Generate dataset version")
        print("4. Train model")
        
    except Exception as e:
        print(f"❌ Lỗi API: {e}")
        print("\nKiểm tra:")
        print("- API key có đúng không?")
        print("- Workspace ID có đúng không?") 
        print("- Project đã được tạo chưa?")
        print("- Kết nối internet có ổn định không?")

def check_dataset():
    """
    Kiểm tra dataset local trước khi upload
    """
    dataset_path = "roboflow_gender_dataset"
    
    print("📊 Kiểm tra dataset local...")
    
    if not os.path.exists(dataset_path):
        print(f"❌ Không tìm thấy: {dataset_path}")
        return False
    
    classes = ["female", "male"]
    total_images = 0
    
    for class_name in classes:
        class_path = os.path.join(dataset_path, class_name)
        if os.path.exists(class_path):
            images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            count = len(images)
            total_images += count
            print(f"   {class_name}: {count} ảnh")
        else:
            print(f"❌ Không tìm thấy class: {class_path}")
            return False
    
    print(f"   Total: {total_images} ảnh")
    
    # Kiểm tra data.yaml
    yaml_path = os.path.join(dataset_path, "data.yaml")
    if os.path.exists(yaml_path):
        print("✅ data.yaml có sẵn")
    else:
        print("⚠️  Không tìm thấy data.yaml")
    
    return True

if __name__ == "__main__":
    print("🔍 Roboflow Python API Upload")
    print("=" * 50)
    
    # Kiểm tra dataset trước
    if not check_dataset():
        print("\n❌ Dataset chưa sẵn sàng. Chạy scripts/upload_cli.sh trước.")
        exit(1)
    
    print("\n" + "=" * 50)
    print("⚠️  CẢNH BÁO: Upload qua API có thể mất nhiều thời gian!")
    print("Với 6,000 ảnh, ước tính: 30-60 phút")
    print("Khuyến nghị: Sử dụng CLI hoặc Web Upload")
    print("=" * 50)
    
    # Hỏi xác nhận
    confirm = input("\nBạn có muốn tiếp tục với API upload? (y/N): ")
    if confirm.lower() not in ['y', 'yes']:
        print("Hủy upload. Sử dụng CLI hoặc Web Upload thay thế.")
        exit(0)
    
    # Upload
    upload_with_python_api()
