# pip install Flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Hello world</h1>'


if __name__ == '__main__':
    app.run(port=5000)
# app.run(debug=True, port=8081)

# sudo docker pull python
# sudo docker build -t class3 .   # class3 kiyanne kamathi namak
# docker run -p 5000:5000 class3
# docker build -t my-app:latest --no-cache .
# https://hub.docker.com/_/python
