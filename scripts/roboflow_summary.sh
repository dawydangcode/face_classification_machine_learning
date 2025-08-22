#!/bin/bash

echo "📋 ROBOFLOW UPLOAD SUMMARY"
echo "=========================="

# Kiểm tra dataset
if [ -d "roboflow_gender_dataset" ]; then
    echo "✅ Dataset sẵn sàng: roboflow_gender_dataset/"
    echo "   📁 Female: $(ls roboflow_gender_dataset/female/ | wc -l) images"
    echo "   📁 Male: $(ls roboflow_gender_dataset/male/ | wc -l) images"
    echo "   📄 data.yaml: $([ -f roboflow_gender_dataset/data.yaml ] && echo "✅" || echo "❌")"
else
    echo "❌ Dataset chưa sẵn sàng"
    echo "Chạy: ./scripts/upload_cli.sh"
    exit 1
fi

echo ""
echo "🚀 CÁC CÁCH UPLOAD"
echo "=================="

echo ""
echo "CÁCH 1: Web Upload (Khuyến nghị - Đơn giản nhất)"
echo "------------------------------------------------"
echo "1. Truy cập: https://roboflow.com"
echo "2. Create New Project > Classification > Single-Label"
echo "3. Project name: gender-classification"
echo "4. Upload folder: roboflow_gender_dataset/"
echo "5. Roboflow tự detect classes: female, male"

echo ""
echo "CÁCH 2: CLI Upload (Nhanh cho dataset lớn)"
echo "-------------------------------------------"
echo "1. Login CLI:"
echo "   source venv/bin/activate"
echo "   roboflow login"
echo "   # Truy cập: https://app.roboflow.com/auth-cli"
echo "   # Copy token và paste"
echo ""
echo "2. Upload:"
echo "   roboflow import -w YOUR_WORKSPACE_ID -p gender-classification roboflow_gender_dataset"

echo ""
echo "CÁCH 3: Python API (Tùy chỉnh cao)"
echo "-----------------------------------"
echo "1. Cập nhật API key trong scripts/upload_python_api.py"
echo "2. Chạy: python3 scripts/upload_python_api.py"

echo ""
echo "📖 Chi tiết"
echo "==========="
echo "📄 Đọc hướng dẫn: ROBOFLOW_UPLOAD_GUIDE.md"
echo "🔧 Scripts có sẵn:"
echo "   - scripts/upload_cli.sh (chuẩn bị CLI)"
echo "   - scripts/upload_python_api.py (API upload)"
echo "   - scripts/upload_to_roboflow.py (tạo dataset)"

echo ""
echo "🎯 SAU KHI UPLOAD"
echo "================="
echo "1. ✅ Review images trên Roboflow"
echo "2. ⚙️  Configure dataset split (70/20/10)"
echo "3. 🔄 Apply augmentation (optional)"
echo "4. 🚀 Train model (30-60 minutes)"
echo "5. 📊 Evaluate accuracy, precision, recall"
echo "6. 🌐 Deploy model for inference"
