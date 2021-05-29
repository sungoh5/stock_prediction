import numpy as np

from flask import Flask, render_template

from app.common import mongo


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    def extract_data(results):
        times = []
        closes = []
        predictions = []

        for item in list(results):
            times.append(item.get('Date').strftime("%Y-%m-%d"))
            closes.append(item.get('Close'))
            predictions.append(item.get('Prediction'))

        return times, closes, predictions, np.around(np.average(closes), 2)

    def get_price_mse(closes, predictions):
        mse_tmp = 0
        distance_tmp = 0
        for i in range(len(closes)):
            mse_tmp += np.power(closes[i] - predictions[i], 2)
            distance_tmp += np.sqrt(np.power(closes[i] - predictions[i], 2))

        return np.around(mse_tmp / len(closes), 2), np.around(distance_tmp / len(closes), 2)

    @app.route("/<ticker>", methods=['GET'])
    def get_prediction(ticker):
        rnn_times = []
        rnn_closes = []
        rnn_predictions = []

        lstm_times = []
        lstm_closes = []
        lstm_predictions = []

        gru_times = []
        gru_closes = []
        gru_predictions = []

        tickers = mongo.client['tickers'].find({'ticker': f'{ticker}'}, {'_id': False})
        if tickers.count() > 0:
            for algo in ('rnn', 'lstm', 'gru'):
                results = mongo.client[f'{ticker}_{algo}_prediction'].find({}, {'_id': False})
                if algo == 'rnn':
                    rnn_times, rnn_closes, rnn_predictions, rnn_close_avg_price = extract_data(results)
                    rnn_mse, rnn_price_distance = get_price_mse(rnn_closes, rnn_predictions)
                elif algo == 'lstm':
                    lstm_times, lstm_closes, lstm_predictions, lstm_close_avg_price = extract_data(results)
                    lstm_mse, lstm_price_distance = get_price_mse(lstm_closes, lstm_predictions)
                else:
                    gru_times, gru_closes, gru_predictions, gru_close_avg_price = extract_data(results)
                    gru_mse, gru_price_distance = get_price_mse(gru_closes, gru_predictions)

            return render_template('line_chart.html', ticker=ticker.upper(), close_legend='close',
                                   prediction_legend='prediction',
                                   rnn_times=rnn_times, rnn_closes=rnn_closes, rnn_predictions=rnn_predictions,
                                   rnn_mse=rnn_mse, rnn_price_distance=rnn_price_distance, rnn_close_avg_price=rnn_close_avg_price,
                                   lstm_times=lstm_times, lstm_closes=lstm_closes, lstm_predictions=lstm_predictions,
                                   lstm_mse=lstm_mse, lstm_price_distance=lstm_price_distance, lstm_close_avg_price=lstm_close_avg_price,
                                   gru_times=gru_times, gru_closes=gru_closes, gru_predictions=gru_predictions,
                                   gru_mse=gru_mse, gru_price_distance=gru_price_distance, gru_close_avg_price=gru_close_avg_price)
        else:
            return f'The {ticker} does not support'

    return app
