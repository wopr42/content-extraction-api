from flask import Flask
from flask_restplus import Api, Resource, fields
from newspaper import Article

app = Flask(__name__)
api = Api(app)

model = api.model('Model', {
    'keywords': fields.List(fields.String),
    'title': fields.String,
    'url': fields.String
})

class ArticleExtraction(object):
    def __init__(self, data):
        self.keywords = data.get('keywords', [])
        self.title = data['title']
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
            'title': article.title,
            'url': url
        }), 201

if __name__ == '__main__':
    app.run(debug=True)
