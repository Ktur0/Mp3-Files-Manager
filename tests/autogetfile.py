import os

# Lấy đường dẫn của file py hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))

# Giả sử folder cần lấy tên là "data"
folder_path = os.path.join(current_dir, "mp3_files")

print(folder_path)