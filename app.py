import rest
import json
from simplexml import dumps
from flask import Flask, make_response
from flask_restful import Api

app = Flask(__name__)

api = Api(app)

#
# source: https://roytuts.com/how-to-return-different-response-formats-json-xml-in-flask-rest-api/
#

@api.representation('application/xml')
def output_xml(data, code, headers=None):
	resp = make_response(dumps({'response' : data}), code)
	resp.headers.extend(headers or {})
	return resp



api.add_resource(rest.GreetName, '/<string:name>')
api.add_resource(rest.GetProfilesListData, '/')

if __name__ == "__main__":
	app.run()