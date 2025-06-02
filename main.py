from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Connect to PostgreSQL database
def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if user exists
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    result = cur.fetchone()

    if result:
        message = "✅ Login successful"
    else:
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            message = "🆕 New user created!"
        except:
            message = "❌ Error creating user"
    
    cur.close()
    conn.close()

    return render_template('result.html', username=username, msg=message)

if __name__ == '__main__':
    app.run()
