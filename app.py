from flask import Flask, render_template, request
import pickle
import numpy as np
import catboost
from catboost import CatBoostRegressor
import datetime

app = Flask(__name__)

model = pickle.load(open("cat_model.pkl", "rb"))

now = datetime.datetime.now()

@app.route("/")
def Home():
    return render_template("home.html")

@app.route("/predict", methods = ["POST"])
def predict():
    d1 = np.log(float(request.form['so'])) #логарифм общей площадь
    d2 = float(request.form['sk']) #площадь кухни
    d3 = float(request.form['sj']) #жилая площадь
    d4 = int(request.form['floor_all']) #этажность дома
    d5 = now.year - int(request.form['age']) #год постройки
    d6 = float(request.form['longitude']) #долгота
    d7 = float(request.form['latitude']) #широта
        
    d8 = request.form['bathroom'] #тип санузла
    if d8 == "совмещенный":
        d8 = 1
    else: 
        d8 = 0

    d9 = request.form['room_size'] #количество комнат
    if d9 == "1к":
        d9_1 = 1
        d9_2 = 0
        d9_3 = 0
        d9_4 = 0
        d9_5 = 0
    elif d9 == "2к":
        d9_1 = 0
        d9_2 = 1
        d9_3 = 0
        d9_4 = 0
        d9_5 = 0
    elif d9 == "3к":
        d9_1 = 0
        d9_2 = 0
        d9_3 = 1
        d9_4 = 0
        d9_5 = 0
    elif d9 == "4к и более":
        d9_1 = 0
        d9_2 = 0
        d9_3 = 0
        d9_4 = 1
        d9_5 = 0
    else:
        d9_1 = 0
        d9_2 = 0
        d9_3 = 0
        d9_4 = 0
        d9_5 = 1

    d10 = request.form['floor'] #этаж
    if d10 == "первый":
        d10_1 = 1
        d10_2 = 0
        d10_3 = 0
    elif d10 == "последний":
        d10_1 = 0
        d10_2 = 1
        d10_3 = 0
    else:
        d10_1 = 0
        d10_2 = 0
        d10_3 = 1

    d11 = request.form['wall_material'] #материал стен
    if d11 == "деревянный":
        d11_1 = 1
        d11_2 = 0
        d11_3 = 0
        d11_4 = 0
    elif d11 == "кирпичный":
        d11_1 = 0
        d11_2 = 1
        d11_3 = 0
        d11_4 = 0
    elif d11 == "монолитный":
        d11_1 = 0
        d11_2 = 0
        d11_3 = 1
        d11_4 = 0
    else:
        d11_1 = 0
        d11_2 = 0
        d11_3 = 0
        d11_4 = 1

    d12 = request.form['finishing_level'] #уровень отделки
    if d12 == "дизайнерский":
        d12_1 = 1
        d12_2 = 0
        d12_3 = 0
        d12_4 = 0
    elif d12 == "евроремонт":
        d12_1 = 0
        d12_2 = 1
        d12_3 = 0
        d12_4 = 0
    elif d12 == "стандартный":
        d12_1 = 0
        d12_2 = 0
        d12_3 = 1
        d12_4 = 0
    else:
        d12_1 = 0
        d12_2 = 0
        d12_3 = 0
        d12_4 = 1

    arr = np.array([[d1, d2, d3, d4, d5, d6, d7, d8, d9_1, d9_2, d9_3, d9_4, d9_5, d10_1, d10_2, d10_3, 
                        d11_1, d11_2, d11_3, d11_4, d12_1, d12_2, d12_3, d12_4]])
    print(arr)
    pred = np.round(np.exp(model.predict(arr)), -3)
    pred = '{0:,}'.format(pred[0]).replace(',', ' ') #округление и разрядность
    
    return render_template("home.html", pred = pred)


if __name__ == "__main__":
    app.run(debug=True)