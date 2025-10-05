from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Render!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render के लिए जरूरी
    app.run(host="0.0.0.0", port=port)
