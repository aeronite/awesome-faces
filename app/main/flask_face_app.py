import cognitive_face
import os
from flask import Flask
from main.analyzer_resource import api

app = Flask(__name__)
api.init_app(app)

cognitive_face.Key.set(os.environ['AZURE_SECRET_KEY'])
cognitive_face.BaseUrl.set(os.environ['AZURE_BASE_URL'])

if __name__ == '__main__':
    app.run()
