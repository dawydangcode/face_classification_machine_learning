# 🚀 Hướng dẫn Upload Dataset lên Roboflow bằng CLI

## Bước 1: Tạo tài khoản và project Roboflow

1. **Truy cập Roboflow**: https://roboflow.com
2. **Đăng ký/Đăng nhập** tài khoản
3. **Tạo project mới**:
   - Click "Create New Project"
   - Chọn "Classification" → "Single-Label"
   - Project name: `gender-classification`
   - Description: "Gender classification using CelebA dataset"

## Bước 2: Lấy thông tin cần thiết

1. **Workspace ID**: Tìm thấy trong URL: `https://app.roboflow.com/{WORKSPACE_ID}/`
2. **Project ID**: Thường giống với project name: `gender-classification`
3. **API Key**: Settings → API → Copy Private API Key

## Bước 3: Login CLI

```bash
# Activate virtual environment
source venv/bin/activate

# Login to Roboflow
roboflow login
```

- Truy cập: https://app.roboflow.com/auth-cli
- Copy authentication token
- Paste vào terminal

## Bước 4: Upload Dataset

```bash
# Upload dataset với CLI
roboflow import -w YOUR_WORKSPACE_ID -p gender-classification roboflow_gender_dataset
```

**Thay thế**:

- `YOUR_WORKSPACE_ID` bằng Workspace ID thực tế của bạn
- `gender-classification` bằng Project ID thực tế

## Bước 5: Verify Upload

Sau khi upload:

1. Truy cập project trên Roboflow.com
2. Kiểm tra 6,000 ảnh đã được upload
3. Verify 2 classes: female (3,000), male (3,000)

## Alternative: Upload bằng Python API

Nếu CLI không hoạt động, có thể sử dụng Python API:

```python
from roboflow import Roboflow

# Initialize Roboflow
rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("YOUR_WORKSPACE").project("gender-classification")

# Upload images programmatically
# (Code sẽ phức tạp hơn cho Classification)
```

## Dataset Structure Đã Chuẩn Bị

```
roboflow_gender_dataset/
├── data.yaml           # Dataset configuration
├── female/             # 3,000 female images
│   ├── 000001.jpg
│   ├── 000002.jpg
│   └── ...
└── male/               # 3,000 male images
    ├── 000003.jpg
    ├── 000004.jpg
    └── ...
```

## Troubleshooting

**Lỗi authentication**:

- Kiểm tra API key và workspace ID
- Đảm bảo đã login CLI thành công

**Lỗi format**:

- Kiểm tra data.yaml syntax
- Đảm bảo folder structure đúng

**Upload chậm**:

- Dataset có 6,000 ảnh, có thể mất 10-30 phút
- Kiểm tra kết nối internet

## Sau khi upload thành công

1. **Generate dataset version**
2. **Configure augmentation** (optional)
3. **Train model**:
   - Model type: Classification
   - Backbone: ResNet, EfficientNet, etc.
   - Training duration: ~30-60 phút
4. **Evaluate results**
5. **Deploy model** cho inference

---

📧 **Cần hỗ trợ?** Liên hệ qua GitHub Issues hoặc Roboflow Support.
