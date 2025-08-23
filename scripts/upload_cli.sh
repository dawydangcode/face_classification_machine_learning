#!/bin/bash

# Script để upload dataset lên Roboflow sử dụng CLI
# Dành cho Single-Label Gender Classification

echo "🚀 Roboflow CLI Upload Script"
echo "================================"

# Kiểm tra xem đã có dataset chưa
if [ ! -d "temp_roboflow_gender" ]; then
    echo "❌ Không tìm thấy thư mục temp_roboflow_gender/"
    echo "Vui lòng chạy scripts/upload_to_roboflow.py trước"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "📁 Chuẩn bị dataset structure..."

# Tạo thư mục dataset theo format Roboflow yêu cầu
DATASET_DIR="roboflow_gender_dataset"
rm -rf $DATASET_DIR
mkdir -p $DATASET_DIR

# Copy dữ liệu
cp -r temp_roboflow_gender/* $DATASET_DIR/

# Tạo data.yaml file cho Single-Label Classification
cat > $DATASET_DIR/data.yaml << EOF
# Roboflow Single-Label Classification Dataset
# Gender Classification: Female vs Male

# Dataset info
roboflow:
  # Roboflow project information
WORKSPACE_ID="faceshapedetect"
PROJECT_ID="gender-classification-uzvfc"
  version: 1

# Number of classes
nc: 2

# Class names (Single-Label Classification)
names:
  0: female
  1: male

# Additional info
task: classification
type: single-label
EOF

echo "✅ Đã tạo data.yaml"
cat $DATASET_DIR/data.yaml

echo ""
echo "🔑 Bước tiếp theo:"
echo "1. Login vào Roboflow:"
echo "   roboflow login"
echo ""
echo "2. Tạo project trên Roboflow.com:"
echo "   - Truy cập https://roboflow.com"
echo "   - Create New Project > Classification > Single-Label"
echo "   - Project name: gender-classification"
echo "   - Lấy WORKSPACE_ID và PROJECT_ID"
echo ""
echo "3. Upload dataset:"
echo "   roboflow import -w YOUR_WORKSPACE_ID -p gender-classification $DATASET_DIR"
echo ""
echo "📋 Dataset summary:"
echo "   Path: $DATASET_DIR/"
echo "   Female images: $(ls $DATASET_DIR/female/ | wc -l)"
echo "   Male images: $(ls $DATASET_DIR/male/ | wc -l)"
echo "   Total: $(($(ls $DATASET_DIR/female/ | wc -l) + $(ls $DATASET_DIR/male/ | wc -l))) images"
