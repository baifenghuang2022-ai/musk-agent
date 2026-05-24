from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

with open(r'C:\Users\90611\Desktop\musk_transcript.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

client = OpenAI(
    api_key="sk-51a28f102670424d92efb042b34ab0cb",
    base_url="https://api.deepseek.com"
)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>马斯克智能体</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        #chat { background: white; border-radius: 10px; padding: 20px; min-height: 400px; margin-bottom: 20px; overflow-y: auto; max-height: 500px; }
        .user { text-align: right; margin: 10px 0; }
        .user span { background: #007bff; color: white; padding: 8px 15px; border-radius: 15px; display: inline-block; }
        .musk { text-align: left; margin: 10px 0; }
        .musk span { background: white; border: 1px solid #ddd; padding: 8px 15px; border-radius: 15px; display: inline-block; max-width: 80%; }
        .name { font-size: 12px; color: #999; margin-bottom: 3px; }
        #input-area { display: flex; gap: 10px; }
        #msg { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>🚀 马斯克智能体</h1>
    <div id="chat"></div>
    <div id="input-area">
        <input id="msg" type="text" placeholder="问马斯克任何问题..." onkeypress="if(event.key==='Enter')send()">
        <button onclick="send()">发送</button>
    </div>
    <script>
        let history = [];
        async function send() {
            const msg = document.getElementById('msg').value.trim();
            if (!msg) return;
            document.getElementById('msg').value = '';
            const chat = document.getElementById('chat');
            chat.innerHTML += `<div class="user"><span>${msg}</span></div>`;
            history.push({role: 'user', content: msg});
            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({history})
            });
            const data = await res.json();
            chat.innerHTML += `<div class="musk"><div class="name">马斯克</div><span>${data.reply}</span></div>`;
            history.push({role: 'assistant', content: data.reply});
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/chat', methods=['POST'])
def chat():
    history = request.json['history']
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"你是马斯克智能体，基于以下访谈内容回答问题。用马斯克的思维方式和语气，第一人称，简洁直接。\n\n访谈内容：{transcript[:8000]}"}
        ] + history
    )
    return jsonify({'reply': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True, port=5000)