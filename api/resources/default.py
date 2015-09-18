from flask_restful import Resource


info = {
    'version': '0.1.0'
}

class Index(Resource):
    def get(self):
        return info
