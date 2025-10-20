from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os

# Khởi tạo Flask app
app = Flask(__name__, static_folder='static')

# Cấu hình API key từ biến môi trường (Render sẽ set qua Environment)
genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'AIzaSyD0Bt0WGMf7yvZrQCYpHx_uoqqv61bZwjE'))

# Chọn model Gemini
model = genai.GenerativeModel('gemini-2.5-flash')

# Prompt tối ưu cho lập trình, trả lời đẹp và rõ ràng
CODING_PROMPT = """
Bạn là trợ lý lập trình chuyên nghiệp. Khi trả lời:
1. Nếu viết code, đặt code trong khối ```language
2. Giải thích code ngắn gọn, dễ hiểu, bằng tiếng Việt.
3. Nếu debug, chỉ ra lỗi cụ thể và cách sửa.
4. Nếu giải thích thuật toán, chia thành các bước logic.
Trả lời bằng tiếng Việt, giữ code bằng tiếng Anh.
"""

# Route chính, trả về giao diện chat
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Route xử lý chat
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'Vui lòng nhập tin nhắn'}), 400

        # Gửi prompt và yêu cầu của user
        response = model.generate_content(CODING_PROMPT + "\nYêu cầu: " + user_message)
        ai_reply = response.text
        return jsonify({'reply': ai_reply})
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

# Chạy app với gunicorn (Render sẽ override)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
