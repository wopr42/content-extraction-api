from flask import Flask
from flask_restplus import Api, Resource, fields
from newspaper import Article

app = Flask(__name__)
api = Api(app)

model = api.model('Model', {
    'keywords': fields.List(fields.String),
    'summary': fields.String,
    'text': fields.String,
    'title': fields.String,
    'top_image': fields.String,
    'url': fields.String
})

class ArticleExtraction(object):
    def __init__(self, data):
        self.keywords = data.get('keywords', [])
        self.summary = data['summary']
        self.text = data['text']
        self.title = data['title']
        self.top_image = data['top_image']
        self.url = data['url']

        self.keywords.sort()

@api.route('/article_extractions', methods=['POST'])
class ArticleExtractions(Resource):
    @api.expect(model)
    @api.marshal_with(model, code=201)
    def post(self):
        url = api.payload['url']
        article = Article(url)

        article.download()
        article.parse()
        article.nlp()

        return ArticleExtraction({
            'keywords': article.keywords,
            'summary': article.summary,
            'text': article.text,
            'title': article.title,
            'top_image': article.top_image,
            'url': url
        }), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
