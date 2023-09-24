from flask import Flask, request , jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    print(source_currency)
    print(amount)
    print(target_currency)

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)

    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }

    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_lfin7OTxfq53Rwa7H5Dmw3xyVsa3fSlHtvqHC1bz&currencies={}&base_currency={}".format(
        target, source)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rates = data.get("data")

        if rates is not None and target in rates:
            return rates[target]

    # Return None if conversion rate is not available or there is an error.
    return None


if __name__ == "__main__":
    app.run(debug=True)
