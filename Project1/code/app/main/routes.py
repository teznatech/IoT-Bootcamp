from flask import jsonify, request, Response, render_template, send_file, url_for
from app import db
from app.models import Data
from app.main import bp
from datetime import date
import pandas as pd

@bp.route('/data/count')
def count_data():
    return jsonify({'Total Rows': Data.query.count()}), 200

@bp.route('/data/<int:id>', methods=['GET'])
def get_data(id):
    return jsonify(Data.query.get_or_404(id).to_dict()), 200

@bp.route('/data', methods=['GET'])
def get_all_data():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return jsonify(Data.to_collection_dict(Data.query,
                    page, per_page, 'main.get_all_data', 
                    order_by=Data.timestamp.desc())), 200

@bp.route('/data/<start>/<end>', methods=['GET'])
def get_data_date(start, end):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    st_date= start.split('-')
    end_date= end.split('-')
    # dates should come in DD-MM-YYYY format
    start = date(year=int(st_date[2]), month=int(st_date[1]), day=int(st_date[0]))
    end = date(year=int(end_date[2]), month=int(end_date[1]), day=int(end_date[0]))
    data = Data.to_collection_dict(
        Data.query.filter(Data.timestamp <= end).filter(Data.timestamp >= start),
        page, per_page, 'main.get_data_date', order_by=Data.timestamp.desc(), 
        start=start, end=end)

    return jsonify(data), 200

csv = '/home/pi/IoT-Bootcamp/Project1/code/app/static/record/dht.csv'
html = '/home/pi/IoT-Bootcamp/Project1/code/app/templates/main/monitor.html'

@bp.route('/data/summary')
def summary():
    #df = pd.read_csv('/home/pi/iot-tutorial/tutorial/app/static/record/dht.csv')
    #df.iloc[-1] = ['Datetime','Temperature','Humidity']
    #df.rename(columns=df.iloc[-1]).drop(df.index[-1])
    df = pd.read_csv(csv)
    return df.describe().to_html()

@bp.route('/monitor')
def montior():
    return render_template('main/monitor.html')

@bp.route('/record/dht.csv')
def records():
    return send_file(csv)

@bp.route('/getView')
def getView():
    return send_file(html)

@bp.route('/test/<test_str>')
def test(test_str):
    return jsonify({'test':test_str}), 200
