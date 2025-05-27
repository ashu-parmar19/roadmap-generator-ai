from flask import Flask, render_template, request, redirect, session, url_for, flash, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from utils.generate_roadmap import generate_roadmap  # Assuming this is a custom module for roadmap generation  
from xhtml2pdf import pisa  # For PDF generation
from io import BytesIO
from dotenv import load_dotenv  # For loading environment variables
from utils.prompt_analyzer import analyze_prompt
# Assuming this is a custom module for prompt analysis
load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
app.secret_key = os.urandom(24)  # for session encryption

# Initialize DB
def init_db():
    conn = sqlite3.connect('users.db')  #this creates a new database file if it doesn't exist
    c = conn.cursor()
    c.execute('''            
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')                                          #creates the table if it doesn't exist
    conn.commit()
    conn.close()

init_db()  # Run once when app starts

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))
            conn.commit()
            conn.close()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('User already exists. Try logging in.', 'danger')

    return render_template('signup.html')

# Login Route
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['email'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            analysis = analyze_prompt(prompt)
            # ✅ Store in session for download
            session['analysis_result'] = analysis

            # ✅ Optionally display message
            flash("✅ Roadmap generated! You can now download the PDF.", 'success')
        else:
            flash("⚠️ Please enter a prompt for analysis.", 'warning')

        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')
    
@app.route('/download-roadmap-pdf')      
def download_pdf():
    analysis = session.get('analysis_result')
    if not analysis:
        flash("⚠️ No analysis result found. Please generate a roadmap first.", 'warning')
        return redirect(url_for('dashboard'))
    roadmap = generate_roadmap(analysis)
    html = render_template('roadmap.html', roadmap=roadmap)

    result = BytesIO()
    pdf_status = pisa.CreatePDF(src=html, dest=result)

    if pdf_status.err:
        flash("⚠️ Error generating PDF.", 'danger')
        return redirect(url_for('dashboard'))
    
    response = make_response(result.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=roadmap.pdf'
    return response


# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)

