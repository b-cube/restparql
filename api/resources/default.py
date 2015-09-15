from flask_restful import Resource
from flask import render_template

info = {
    'version': '0.1.0'
}

class Index(Resource):
    def get(self):
        return render_template('index.html',
                               info=info)
