# Face Classification Machine Learning

Dự án phân loại giới tính và các đặc điểm khuôn mặt sử dụng Machine Learning với dataset CelebA.

## Mô tả

Dự án này sử dụng dataset CelebA (Large-scale CelebFaces Attributes) để phân loại:

- **Giới tính**: Nam/Nữ
- **Màu da**: Sáng/Trung bình/Tối
- **Dáng mặt**: Oval/Tròn/Vuông/Trái tim/Kim cương

## Dataset

- **Nguồn**: CelebA Dataset từ The Chinese University of Hong Kong
- **Số lượng**: 202,599 ảnh khuôn mặt người nổi tiếng
- **Kích thước ảnh**: 218x178 pixels (đã được căn chỉnh và crop)
- **Annotations**: 40 thuộc tính nhị phân + 5 landmark points

## Cấu trúc dự án

```
gender-detection/
├── data/
│   ├── raw/                    # Dữ liệu thô từ CelebA
│   ├── train/                  # Dữ liệu training
│   └── test/                   # Dữ liệu testing
├── models/                     # Các model đã train
├── scripts/
│   ├── prepare_data.py         # Script xử lý và chuẩn bị dữ liệu
│   ├── train_model.py          # Script training model
│   └── predict.py              # Script dự đoán
├── requirements.txt            # Dependencies
└── README.md
```

## Cài đặt

1. Clone repository:

```bash
git clone https://github.com/dawydangcode/face_classification_machine_learning.git
cd face_classification_machine_learning
```

2. Tạo virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows
```

3. Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

4. Tải dataset CelebA và đặt vào thư mục `data/raw/`

## Sử dụng

### Chuẩn bị dữ liệu

```bash
python3 scripts/prepare_data.py
```

### Training model

```bash
python3 scripts/train_model.py
```

### Dự đoán

```bash
python3 scripts/predict.py --image path/to/image.jpg
```

## Đặc điểm kỹ thuật

### Thuật toán phân loại dáng mặt

- Sử dụng 5 landmark points từ CelebA
- Tính toán tỷ lệ chiều rộng/chiều cao khuôn mặt
- Phân tích tỷ lệ chiều rộng hàm
- Thuật toán hash-based để đảm bảo phân bố cân bằng (20% mỗi loại)

### Phân loại màu da

- Phân tích giá trị RGB trung bình
- Phân loại thành 3 cấp độ: Sáng/Trung bình/Tối

## Kết quả

Dataset sau xử lý có phân bố cân bằng:

- Mỗi dáng mặt: ~20%
- Gender: ~50% nam, ~50% nữ
- Màu da: Phân bố đa dạng

## Tác giả

- Dawy Dang

## License

Dự án chỉ được sử dụng cho mục đích nghiên cứu và giáo dục, tuân theo điều khoản của CelebA dataset.

## Trích dẫn

Nếu sử dụng trong nghiên cứu, vui lòng trích dẫn:

```
@inproceedings{liu2015faceattributes,
  author = {Ziwei Liu, Ping Luo, Xiaogang Wang, and Xiaoou Tang},
  title = {Deep Learning Face Attributes in the Wild},
  booktitle = {Proceedings of International Conference on Computer Vision (ICCV)},
  month = December,
  year = {2015}
}
```
