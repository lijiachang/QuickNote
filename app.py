from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)


# 创建数据库
def init_db():
    conn = sqlite3.connect('notes.db')
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
<body>
    <form method="post">
        <textarea name="content" rows="4" cols="50"></textarea><br>
        <input type="submit" value="保存">
    </form>
    <h3>历史记录:</h3>
    {% for note in notes %}
        <div style="margin-bottom: 10px">
            <div>{{ note[2] }}</div>
            <pre>{{ note[1] }}</pre>
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
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute('INSERT INTO notes (content, created_at) VALUES (?, ?)',
                  (content, datetime.now()))
        conn.commit()
        conn.close()

    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    notes = c.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
    conn.close()

    return render_template_string(HTML, notes=notes)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)