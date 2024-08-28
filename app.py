from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    technologies = {
        "server": response.headers.get('Server'),
        "html_meta": [],
        "scripts": [],
        "links": [],
    }

    # Analyze HTML meta tags
    for meta in soup.find_all('meta'):
        technologies["html_meta"].append(meta.get('name'))

    # Analyze scripts
    for script in soup.find_all('script', src=True):
        technologies["scripts"].append(script.get('src'))

    # Analyze links
    for link in soup.find_all('link', href=True):
        technologies["links"].append(link.get('href'))

    return jsonify(technologies)

if __name__ == '__main__':
    app.run(debug=True)
