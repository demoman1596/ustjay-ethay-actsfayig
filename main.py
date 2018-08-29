import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

TEMPLATE = '''<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <p><b>Fact:</b> {}</p>
        <p><b>Translation to Pig Latin:</b> <a href="{}">{}</a></p>
    </body>
</html>'''

def get_fact():
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


@app.route('/')
def home():
    fact = get_fact()
    response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/", data = {'input_text':fact}, allow_redirects=False)
    return TEMPLATE.format(fact, response.headers['Location'], response.headers['Location'])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

