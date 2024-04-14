import time
import requests
import subprocess
import random
import string
import os


def capture_image(output_dir):
    try:
        image_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".jpg"
        image_path = os.path.join(output_dir, image_name)
        subprocess.run(["fswebcam", "-r", "640x480", "--no-banner", image_path], check=True)
        return image_path
    except subprocess.CalledProcessError:
        print("Lỗi khi chụp ảnh.")
        return None


def send_image_to_server(image_path, server_url, download_dir):
    files = {'file': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')}
    try:
        response = requests.post(f"{server_url}/upload", files=files)
        if response.status_code == 200:
            data = response.json()
            image_name = data["image_path"].split('\\')[1]
            download_file_from_server(image_name, download_dir)
        else:
            print("Lỗi khi gửi ảnh lên server. Mã lỗi:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Lỗi kết nối tới server:", e)


def download_file_from_server(file_name, download_dir):
    try:
        url = f"{server_url}/images/{file_name}"
        response = requests.get(url)
        if response.status_code == 200:
            download_path = os.path.join(download_dir, file_name)
            with open(download_path, 'wb') as file:
                file.write(response.content)
            print(f"Tệp {file_name} đã được tải xuống thành công.")
        else:
            print(f"Lỗi: Không thể tải xuống tệp {file_name}. Mã lỗi: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Lỗi kết nối tới server:", e)


# Địa chỉ URL của server
server_url = "http://103.3.247.61:5055"
# Thư mục lưu trữ ảnh đã chụp
capture_dir = "capture_images"
# Thư mục lưu trữ ảnh tải về từ server
download_dir = "downloaded_images"

# Tạo các thư mục nếu chưa tồn tại
os.makedirs(capture_dir, exist_ok=True)
os.makedirs(download_dir, exist_ok=True)

# Thực hiện vòng lặp chụp ảnh, gửi lên server và lưu kết quả
while True:
    image_path = capture_image(capture_dir)
    if image_path:
        send_image_to_server(image_path, server_url, download_dir)
    time.sleep(5)