from flask import Flask, render_template, request
import joblib
import sqlite3

app = Flask(__name__)

model = joblib.load("model/phishing_model.pkl")
print("AI model loaded successfully")
def extract_features(url):

    url_length = -1 if len(url) > 75 else 1

    has_https = 1 if "https" in url else -1

    has_at = -1 if "@" in url else 1

    has_dash = -1 if "-" in url else 1

    has_ip = -1 if any(char.isdigit() for char in url.split(':')[0]) else 1

    has_double_slash = -1 if "//" in url[8:] else 1

    subdomain = -1 if url.count('.') > 2 else 1

    features = [
        has_ip,
        url_length,
        1,
        has_at,
        has_double_slash,
        has_dash,
        subdomain,
        has_https,

        -1,-1,-1,-1,-1,-1,-1,-1,
        -1,-1,-1,-1,-1,-1,-1,-1,
        -1,-1,-1,-1,-1,-1
    ]

    return features
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    # Total scans
    cursor.execute("SELECT COUNT(*) FROM scans")
    total_scans = cursor.fetchone()[0]

    # Safe websites
    cursor.execute(
        "SELECT COUNT(*) FROM scans WHERE result='Legitimate Website ✅'"
    )
    safe_sites = cursor.fetchone()[0]

    # Dangerous websites
    cursor.execute(
        "SELECT COUNT(*) FROM scans WHERE result='Phishing Website ❌'"
    )
    dangerous_sites = cursor.fetchone()[0]

    # Recent history
    cursor.execute(
        "SELECT url,result,score FROM scans ORDER BY rowid DESC LIMIT 10"
    )
    history = cursor.fetchall()

    conn.close()

    accuracy = 96

    return render_template(
        "dashboard.html",
        total_scans=total_scans,
        safe_sites=safe_sites,
        dangerous_sites=dangerous_sites,
        accuracy=accuracy,
        history=history
    )
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/save_feedback', methods=['POST'])
def save_feedback():

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('feedback.db')

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO feedback (name,email,message) VALUES (?,?,?)",
        (name,email,message)
    )

    conn.commit()

    conn.close()
    return render_template("success.html")
@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']

    features = extract_features(url)

    prediction = model.predict([features])[0]

    probability = model.predict_proba([features])[0]
    score = round(max(probability) * 100)

    print("URL=", url)
    print("Features=", features)
    print("Prediction=", prediction)
    if prediction == 1:
        result = "Legitimate Website ✅"
    else:
        result = "Phishing Website ❌"

    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scans(url,result,score) VALUES(?,?,?)",
        (url, result, score)
    )

    conn.commit()
    conn.close()

    return render_template(
        'result.html',
        prediction=result,
        score=score
    )

if __name__ == '__main__':
    app.run(debug=True)
