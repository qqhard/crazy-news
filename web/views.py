from web import app
from flask import render_template

@app.route('/')
def index():
    news = [
        {
            'title':'test1',
            'info':'info1info1info1'
        }
    ]
    news = []
    for i in range(5):
        news.append({
            'title':'test'+str(i),
            'info':'info1info1info1'+str(i),
            'link':'link'+str(i)
        })
    return render_template('index.html',news = news)
