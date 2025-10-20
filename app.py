from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Cấu hình API key
genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'AIzaSyD0Bt0WGMf7yvZrQCYpHx_uoqqv61bZwjE'))

model = genai.GenerativeModel('gemini-pro')

# Prompt tối ưu cho coding
CODING_PROMPT = """
Bạn là một trợ lý lập trình chuyên nghiệp. Khi trả lời:
1. Nếu yêu cầu viết code, trả về code trong khối ```language (ví dụ ```python).
2. Giải thích code rõ ràng, ngắn gọn.
3. Nếu debug, chỉ ra lỗi và cách sửa.
4. Nếu giải thích thuật toán, trình bày từng bước.
Trả lời bằng tiếng Việt, trừ code giữ nguyên tiếng Anh.
"""

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Không có tin nhắn'}), 400
    
    try:
        # Gửi prompt kèm yêu cầu user
        response = model.generate_content(CODING_PROMPT + "\nYêu cầu: " + user_message)
        ai_reply = response.text
        return jsonify({'reply': ai_reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
