from flask import Flask
from flask import request
from newspaper import Article

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/article_extractions')
def extract():
    url = request.args.get('url', '')
    article = Article(url)
    article.download()
    article.parse()
    return article.title
