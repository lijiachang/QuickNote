from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# 数据库路径
DB_PATH = os.path.join('data', 'notes.db')


# 创建数据库
def init_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  content TEXT,
                  created_at TIMESTAMP)''')
    conn.commit()
    conn.close()


# HTML模板
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>QuickNote</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            max-width: 800px;
            margin: 20px auto;
            padding: 0 20px;
            font-family: Arial, sans-serif;
        }
        textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .note {
            margin-bottom: 20px;
        }
        .date {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        .content {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 4px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <form method="post">
        <textarea name="content" rows="4" cols="50" placeholder="输入文本..."></textarea><br>
        <input type="submit" value="保存">
    </form>
    <h3>历史记录:</h3>
    {% for note in notes %}
        <div class="note">
            <div class="date">{{ note[2] }}</div>
            <pre class="content">{{ note[1] }}</pre>
            <hr>
        </div>
    {% endfor %}
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        content = request.form['content']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO notes (content, created_at) VALUES (?, ?)',
                  (content, datetime.now()))
        conn.commit()
        conn.close()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    notes = c.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
    conn.close()

    return render_template_string(HTML, notes=notes)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=80)