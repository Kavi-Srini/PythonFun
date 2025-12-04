from flask import Flask

app = Flask(__name__)

@app.route("/")
def greeting():
    return "Welcome to The Spiced Mocha!"

if __name__ == "__main__":
    app.run()
