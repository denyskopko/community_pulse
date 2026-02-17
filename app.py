from flask import Flask

from core.app_runner import create_app

app = Flask(__name__)

create_app(app)

@app.route('/')
def index():
    return 'Welcome to Community Pulse'

if __name__ == '__main__':
    app.run()
