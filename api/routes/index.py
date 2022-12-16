from flask_restful import Resource


# Now we make classes that are subclasses of the Resource

class Index(Resource):
    def get(self):
      return {"hello": "world"}

