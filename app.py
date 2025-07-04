from flask import Flask, render_template, request, redirect, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = "super-uper-duper-secure-key"

app.secret_key = os.environ.get("SECRET_KEY", "fallback-insecure-key")

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'submission_count' not in session:
        session['submission_count'] = 0

    horoscope = None
    sign = None
    date = None

    if request.method == 'POST':
        session['submission_count'] += 1

        if session['submission_count'] > 2:
            return redirect(url_for('pricing'))

        sign = request.form.get('sign')
        day = request.form.get('day', 'TODAY')

        if sign:
            response = requests.get("https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily", params={
                'sign': sign,
                'day': day
            })
            if response.status_code == 200:
                data = response.json().get("data", {})
                horoscope = data.get("horoscope_data", "No message available.")
                date = data.get("date", "")

    return render_template('index.html', horoscope=horoscope, sign=sign, date=date)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/scam-warning')
def scam_warning():
    session['submission_count'] = 0
    return render_template('scam.html')

if __name__ == "__main__":
    app.run()

