# Sử dụng image Python 3.10 mỏng nhẹ
FROM python:3.10-slim

# Đặt thư mục làm việc
WORKDIR /app

# Copy và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn vào container
COPY . .

# Chạy ứng dụng dưới người dùng không có quyền root
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

# Chạy ứng dụng
CMD ["python", "main.py"]
