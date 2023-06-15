from flask import Flask
from models.screen import ScreenFactory
from flask_cors import CORS

DEFAULT_MINIMUM_SYMBOL_MATCHES_FOR_CLUSTER = 5
DEFAULT_PAYOUT_RATIO = 0.032
DEFAULT_MATRIX_DIMENSIONS = [7, 7]

app = Flask('Devour Slots')
CORS(app)

@app.route("/", methods=['GET'])
def get_screen():
    test = ScreenFactory.build(*DEFAULT_MATRIX_DIMENSIONS, DEFAULT_MINIMUM_SYMBOL_MATCHES_FOR_CLUSTER,
                               DEFAULT_PAYOUT_RATIO)
    for combination in test.clusters:
        for symbol in combination:
            test.reels[symbol[1][0], symbol[1][1]].isMatched = True

    print(test)

    return test.generate_response_dto()


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)

