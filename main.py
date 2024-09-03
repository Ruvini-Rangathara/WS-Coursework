# pip install Flask
from flask import Flask
from controller.auth_controller import auth_blueprint
from database import engine, Base

app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Hello world</h1>'


app.register_blueprint(auth_blueprint, url_prefix='/auth')

# Create all tables
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    app.run(port=5000)
# app.run(debug=True, port=8081)

# sudo docker pull python
# sudo docker build -t class3 .   # class3 kiyanne kamathi namak
# docker run -p 5000:5000 class3
# docker build -t my-app:latest --no-cache .
# https://hub.docker.com/_/python
