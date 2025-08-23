#!/usr/bin/env python3
"""
Test Roboflow Gender Classification Model
Sử dụng model đã train trên Roboflow để predict gender từ ảnh
"""

import os
import cv2
from inference import get_model
import supervision as sv

def test_gender_classification():
    """Test gender classification model với ảnh local"""
    
    # Cấu hình model ID - ĐÃ CẬP NHẬT
    model_id = "gender-classification-uzvfc/1"  # Format: project/version
    
    # Kiểm tra API key
    if not os.getenv('ROBOFLOW_API_KEY'):
        print("❌ Lỗi: Chưa set ROBOFLOW_API_KEY")
        print("Chạy: export ROBOFLOW_API_KEY='lde2hp1C5PxcfTaUwjox'")
        return
    
    print("🚀 Loading model...")
    try:
        # Load model từ Roboflow
        model = get_model(model_id=model_id)
        print(f"✅ Model loaded: {model_id}")
    except Exception as e:
        print(f"❌ Lỗi load model: {e}")
        return
    
    # Test với một số ảnh trong dataset
    test_images = [
        "data/raw/Img/img_align_celeba/000001.jpg",
        "data/raw/Img/img_align_celeba/000002.jpg", 
        "data/raw/Img/img_align_celeba/000003.jpg",
        "data/raw/Img/img_align_celeba/000010.jpg",
        "data/raw/Img/img_align_celeba/000020.jpg"
    ]
    
    print("\n📸 Testing gender classification:")
    print("-" * 50)
    
    for img_path in test_images:
        if not os.path.exists(img_path):
            print(f"⚠️  Không tìm thấy: {img_path}")
            continue
            
        try:
            # Đọc ảnh
            image = cv2.imread(img_path)
            if image is None:
                print(f"❌ Không đọc được ảnh: {img_path}")
                continue
            
            # Chạy inference
            print(f"🔍 Testing: {os.path.basename(img_path)}...")
            results = model.infer(image)[0]
            
            # Lấy prediction
            if hasattr(results, 'predicted_classes'):
                predicted_class = results.predicted_classes[0]
                confidence = results.predictions[predicted_class].confidence
                print(f"   Prediction: {predicted_class}")
                print(f"   Confidence: {confidence:.3f}")
            elif hasattr(results, 'class_name'):
                print(f"   Prediction: {results.class_name}")
                print(f"   Confidence: {results.confidence:.3f}")
            else:
                print(f"   Results: {results}")
            
        except Exception as e:
            print(f"❌ Lỗi predict {img_path}: {e}")
        
        print()

def test_single_image(image_path):
    """Test với một ảnh cụ thể"""
    
    model_id = "faceshapedetect/gender-classification-uzvfc"
    
    if not os.getenv('ROBOFLOW_API_KEY'):
        print("❌ Lỗi: Chưa set ROBOFLOW_API_KEY")
        return
        
    if not os.path.exists(image_path):
        print(f"❌ Không tìm thấy ảnh: {image_path}")
        return
    
    print(f"🚀 Loading model và testing: {image_path}")
    
    try:
        # Load model
        model = get_model(model_id=model_id)
        
        # Đọc ảnh
        image = cv2.imread(image_path)
        
        # Predict
        results = model.infer(image)[0]
        
        print("📊 Results:")
        print(f"   File: {os.path.basename(image_path)}")
        
        # Parse results tùy theo format
        if hasattr(results, 'predicted_classes'):
            predicted_class = results.predicted_classes[0]
            confidence = results.predictions[predicted_class].confidence
            print(f"   Gender: {predicted_class}")
            print(f"   Confidence: {confidence:.3f}")
        elif hasattr(results, 'class_name'):
            print(f"   Gender: {results.class_name}")
            print(f"   Confidence: {results.confidence:.3f}")
        else:
            print(f"   Raw results: {results}")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    import sys
    
    print("🎯 Roboflow Gender Classification Test")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Test với ảnh cụ thể
        image_path = sys.argv[1]
        test_single_image(image_path)
    else:
        # Test với multiple ảnh
        test_gender_classification()
