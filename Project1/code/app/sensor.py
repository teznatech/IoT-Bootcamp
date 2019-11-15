import Adafruit_DHT
import threading
from app.models import Data
from app import db
from plotly.offline import plot
import plotly.graph_objs as go
import csv, time, datetime
import os, gzip, shutil


class Sensor():

    def __init__(self, app, sensor=Adafruit_DHT.DHT22, pin=4):
        self.DHT_SENSOR = sensor
        self.DHT_PIN = pin
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.record_file = os.path.join(self.basedir, 'static', 'record', 'dht.csv')
        self.htmlfile = os.path.join(self.basedir, 'templates', 'main', 'monitor.html')
        #self.thread = threading.Timer(60.0, self.read_data).start()


    def read_data(self):
        threading.Timer(60.0, self.read_data).start()
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        if humidity is not None and temperature is not None\
         and humidity < 101 and humidity > 0:
            temperature = '{0:.2f}'.format(temperature)
            humidity = '{0:.2f}'.format(humidity)
            with self.app.app_context():
                if Data.query.count() > 10000:
                    Data.query.delete()

                data = Data(temperature=temperature, humidity=humidity)
                db.session.add(data)
                db.session.commit()
                data = []
                date = time.strftime('%Y-%m-%d %H:%M')
                data.append(date)
                data.append(temperature)
                data.append(humidity)
                #write to data file
                with open(self.record_file, "a") as f_data:
                    wr = csv.writer(f_data)
                    wr.writerow(data)
                self.write_html()

    def write_html(self):
        graphData = []
        with open(self.record_file, "r") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                graphData.append(row)

        date = []
        temp = []
        hum = []
        for item in graphData:
            date.append(item[0])
            temp.append(item[1])
            hum.append(item[2])

        trace1 = go.Scatter(
                x = date,
                y = temp,
                mode = 'lines',
                name = 'Temperature °C',
                line = dict (
                    width = 2,
                    color = ('rgb(217, 0, 0)')))

        trace2 = go.Scatter(
                x = date,
                y = hum,
                mode = 'lines',
                name = 'Humidity %',
                line = dict (
                    width = 2,
                    color = ('rgb(0, 210, 255)')))

        fig = [trace1, trace2]
        layout = go.Layout(
        paper_bgcolor = 'rgb(235, 235, 235)',
        plot_bgcolor = 'rgb(255, 255, 255)',
        title = "Latest Reading: {2} - Temperature {0}°C / Humidity {1}%".format(temp[-1], 
                hum[-1], date[-1]),
        xaxis = dict(
                title="Date",
                type="date",
                autorange=True,
                linewidth = 2,
                showgrid=True,
                tickformat = '%d %B<br>%H:%M:%S'
            ),
        yaxis = dict(
                title="Measure",
                autorange=True,
                linewidth = 2,
                showgrid=True,
            )
        )

        #offline plot to html file
        plot({"data": fig,"layout": layout},filename=self.htmlfile,auto_open=False)



    
