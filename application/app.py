from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from ECS Fargate! 🚀"

@app.route("/healthz")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
