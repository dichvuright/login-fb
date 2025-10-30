# Facebook Auth API

API đơn giản để đăng nhập Facebook với hỗ trợ proxy và batch login.

## 🚀 Tính năng

- ✅ Đăng nhập Facebook đơn lẻ
- ✅ Đăng nhập hàng loạt (batch)
- ✅ Hỗ trợ proxy tự động (random từ file)
- ✅ Random User-Agent cho mỗi request
- ✅ Xử lý các lỗi phổ biến (checkpoint, captcha, sai mật khẩu)

## 📦 Cài đặt

```bash
pip install flask requests
```

## 🔧 Cấu hình

### 1. File proxy.txt
Tạo file `proxy.txt` với format:
```
ip:port:username:password
```

Ví dụ:
```
103.183.118.206:41975:wuut9o8b:wUUT9o8b
103.139.44.100:61056:ugun8y6n:uGuN8y6N
```

### 2. Chạy server

```bash
python app.py
```

Server sẽ chạy tại: `http://0.0.0.0:5[object Object] Endpoints

### 1. Đăng nhập đơn lẻ

**Endpoint:** `POST /api/v1/auth`

**Request Body:**
```json
{
  "username": "email/phone/uid",
  "password": "password"
}
```

**Response thành công:**
```json
{
  "status": "success",
  "msg": "username|password| Đăng nhập thành công",
  "access_token": "...",
  "uid": "...",
  "session_key": "...",
  "status_code": 200
}
```

**Response lỗi:**
```json
{
  "status": "error",
  "msg": "username|password| Thông tin đăng nhập không chính xác",
  "error_subcode": 1348131,
  "status_code": 401
}
```

### 2. Đăng nhập hàng loạt

**Endpoint:** `POST /api/v1/auth/batch`

**Request Body:**
```json
{
  "accc": "tk1|mk1\ntk2|mk2\ntk3|mk3"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Đã xử lý 3 tài khoản",
  "summary": {
    "total": 3,
    "success": 2,
    "failed": 1
  },
  "results": [
    {
      "index": 1,
      "username": "tk1",
      "status": "success",
      "msg": "tk1|mk1| Đăng nhập thành công"
    },
    {
      "index": 2,
      "username": "tk2",
      "status": "error",
      "msg": "tk2|mk2| Thông tin đăng nhập không chính xác"
    }
  ]
}
```

## 🔍 Các mã lỗi phổ biến

| Error Subcode | Ý nghĩa |
|---------------|---------|
| 1348023 | Bị dính captcha spam |
| 1348162 | Checkpoint - Cần phê duyệt đăng nhập |
| 1348131 | Thông tin đăng nhập không chính xác |

## 📝 Ví dụ sử dụng

### cURL - Đăng nhập đơn

```bash
curl -X POST http://localhost:5001/api/v1/auth \
  -H "Content-Type: application/json" \
  -d '{"username":"your_email","password":"your_password"}'
```

### cURL - Đăng nhập batch

```bash
curl -X POST http://localhost:5001/api/v1/auth/batch \
  -H "Content-Type: application/json" \
  -d '{"accc":"email1|pass1\nemail2|pass2\nemail3|pass3"}'
```

### Python

```python
import requests

# Đăng nhập đơn
response = requests.post('http://localhost:5001/api/v1/auth', json={
    'username': 'your_email',
    'password': 'your_password'
})
print(response.json())

# Đăng nhập batch
response = requests.post('http://localhost:5001/api/v1/auth/batch', json={
    'accc': 'email1|pass1\nemail2|pass2\nemail3|pass3'
})
print(response.json())
```

## ⚙️ Cách hoạt động Proxy

- Mỗi request sẽ **random chọn 1 proxy** từ `proxy.txt`
- Nếu không có file proxy hoặc proxy lỗi, request vẫn được gửi (không dùng proxy)
- Proxy format: `ip:port:username:password` hoặc `ip:port` (không auth)

## 📌 Lưu ý

- API này chỉ dùng cho mục đích học tập và nghiên cứu
- Không lạm dụng để spam hoặc vi phạm điều khoản Facebook
- Proxy tốt sẽ giúp tránh bị block IP

## 📄 License

DichVuRight Studio

