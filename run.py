from flask import Flask

app = Flask(__name__)


@app.route('/')
def homepage():
    return "Minha primeira página flask"


if __name__ == "__main__":
    app.run(debug=True)
