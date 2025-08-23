#!/usr/bin/env python3
"""
Script để lấy thông tin workspace từ Roboflow API
"""
import requests
import json

# API Key từ bạn
PRIVATE_API_KEY = "lde2hp1C5PxcfTaUwjox"

def get_workspace_info():
    """Lấy thông tin workspace từ Roboflow API"""
    url = "https://api.roboflow.com/v1/workspaces"
    
    headers = {
        "Authorization": f"Bearer {PRIVATE_API_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        workspaces = response.json()
        
        print("🔍 Thông tin Workspace:")
        print("=" * 50)
        
        for workspace in workspaces.get('workspaces', []):
            print(f"Workspace Name: {workspace.get('name', 'N/A')}")
            print(f"Workspace ID: {workspace.get('id', 'N/A')}")
            print(f"URL: {workspace.get('url', 'N/A')}")
            print("-" * 30)
        
        return workspaces
        
    except requests.RequestException as e:
        print(f"❌ Lỗi khi gọi API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi parse JSON: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Đang lấy thông tin workspace từ Roboflow...")
    get_workspace_info()
