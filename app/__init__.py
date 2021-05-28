import numpy as np

from flask import Flask, render_template

from app.common import mongo


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    def extract_data(ticker):
        times = []
        closes = []
        predictions = []

        results = mongo.client[f'{ticker}_prediction'].find({}, {'_id': False})
        for item in list(results):
            times.append(item.get('Date').strftime("%Y-%m-%d"))
            closes.append(item.get('Close'))
            predictions.append(item.get('Prediction'))

        return times, closes, predictions

    @app.route("/<ticker>", methods=['GET'])
    def get_prediction(ticker):
        tickers = mongo.client['tickers'].find({'ticker': f'{ticker}'}, {'_id': False})
        if tickers.count() > 0:
            times, closes, predictions = extract_data(ticker)
            avg_diff=np.sqrt(np.power(np.mean(closes) - np.mean(predictions), 2))

            return render_template('line_chart.html', ticker=ticker.upper(), labels=times,
                                   closes=closes, close_legend='close',
                                   predictions=predictions, prediction_legend='prediction',
                                   avg_diff=avg_diff)
        else:
            return f'The {ticker} does not support'

    return app
