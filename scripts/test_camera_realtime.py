#!/usr/bin/env python3
"""
Real-time Gender Detection với Camera Laptop
Sử dụng Roboflow model đã train để detect giới tính qua webcam
"""

import cv2
import requests
import base64
import json
import numpy as np
import time

# Roboflow API configuration
API_KEY = "lde2hp1C5PxcfTaUwjox"
MODEL_ID = "faceshapedetect/gender-classification-uzvfc/1"
API_URL = f"https://detect.roboflow.com/{MODEL_ID}"

def encode_image(image):
    """Encode image to base64 for API"""
    _, buffer = cv2.imencode('.jpg', image)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64

def predict_gender(image):
    """Gửi ảnh tới Roboflow API để predict gender"""
    try:
        img_base64 = encode_image(image)
        
        # Gửi request tới API
        response = requests.post(
            API_URL,
            params={"api_key": API_KEY},
            data=img_base64,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None

def draw_prediction(image, prediction):
    """Vẽ kết quả prediction lên ảnh"""
    if prediction and 'predictions' in prediction:
        pred = prediction['predictions']
        
        if pred:  # Nếu có prediction
            # Lấy class và confidence
            gender = pred[0]['class'] if pred else "Unknown"
            confidence = pred[0]['confidence'] if pred else 0
            
            # Màu sắc theo giới tính
            color = (255, 105, 180) if gender.lower() == 'female' else (30, 144, 255)  # Pink for female, Blue for male
            
            # Vẽ text
            text = f"{gender.upper()}: {confidence:.1%}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.2
            thickness = 2
            
            # Tính toán vị trí text
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            
            # Vẽ background cho text
            cv2.rectangle(image, 
                         (10, 10), 
                         (text_width + 20, text_height + baseline + 20), 
                         color, -1)
            
            # Vẽ text
            cv2.putText(image, text, (15, text_height + 15), 
                       font, font_scale, (255, 255, 255), thickness)
            
            # Vẽ frame border
            cv2.rectangle(image, (0, 0), (image.shape[1]-1, image.shape[0]-1), color, 3)
            
        else:
            # Không detect được face
            cv2.putText(image, "No Face Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return image

def main():
    """Main function để chạy real-time gender detection"""
    print("🎥 Starting Real-time Gender Detection...")
    print("📷 Initializing camera...")
    
    # Khởi tạo camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("✅ Camera initialized successfully!")
    print("🚀 Starting detection... (Press 'q' to quit)")
    
    # Variables để control prediction frequency
    last_prediction_time = 0
    prediction_interval = 1.0  # Predict mỗi 1 giây
    current_prediction = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Cannot read frame")
            break
        
        # Flip ảnh để như mirror
        frame = cv2.flip(frame, 1)
        
        # Predict mỗi prediction_interval giây
        current_time = time.time()
        if current_time - last_prediction_time > prediction_interval:
            print("🔍 Predicting...")
            current_prediction = predict_gender(frame)
            last_prediction_time = current_time
        
        # Vẽ prediction lên frame
        frame = draw_prediction(frame, current_prediction)
        
        # Thêm instructions
        cv2.putText(frame, "Press 'q' to quit", 
                   (frame.shape[1] - 180, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Hiển thị frame
        cv2.imshow('Gender Detection - Real Time', frame)
        
        # Check cho quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Camera closed. Thanks for testing!")

if __name__ == "__main__":
    main()
