from flask import Flask, jsonify
from flask_cors import CORS
from scraperservices.DataScraper import scrape_independent

def api_endpoint(): # Create API endpoint
    app = Flask(__name__)
    CORS(app)
    app.config['JSON_AS_ASCII'] = False

    @app.route('/flyerscraperapi/v1', methods=["GET"])
    def fetch_deals(): # Call scraper method
        deals = scrape_independent()
        return jsonify(deals)

    app.run(debug=True)

if __name__ == "__main__":
    api_endpoint()