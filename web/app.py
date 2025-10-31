from flask import *
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"
BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json"


def get_currency_data():
    url = BASE_URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['usd']
    except requests.exceptions.RequestException:
        return {}
rates = get_currency_data()
# Фіктивні курси валют (до 1 USD)
# rates = {
#     "USD": 1.0,
#     "EUR": 0.93,
#     "UAH": 36.9,
#     "GBP": 0.81
# }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    Give_currency = None
    Get_currency = None
    try:
        info = session.get("trade").split("/")
        if info:
            print(info)
            Give_currency = info[0]
            Get_currency = info[1]
    except:
        print("Помилка сесії")
        Give_currency = "usd"
        Get_currency = "uah"
    if request.method == "POST":
        amount = float(request.form.get("amount", 0))
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")
        Get_currency = to_currency
        Give_currency = from_currency
        if from_currency in rates and to_currency in rates:
            usd_amount = amount / rates[from_currency]  # конвертуємо в USD
            result = round(usd_amount * rates[to_currency], 2)
            session["trade"] = f"{Give_currency}/{Get_currency}"
    
    return render_template("index.html", result=result, rates=rates, gft = Give_currency, rsv = Get_currency )

if __name__ == "__main__":
    app.run(debug=True)
