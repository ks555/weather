# -*- coding: UTF-8 -*

import requests
import argparse
import datetime
from cerecloud_rest import CereprocRestAgent
import utils
import json
from xml.etree import ElementTree as ET
from lxml import etree, html
from bs4 import BeautifulSoup
import pytz
import csv

class YrForecast:

    def __init__(self, station, language, time_frame_count=2):
        self.station = station
        self.language = language
        self.time_frame_count = time_frame_count


    def create_forecast_string(self):
        url = utils.get_yr_URL(self.station)
        response = requests.get(url)
        html = response.content
        self.bs = BeautifulSoup(html, 'lxml')
        self.get_current_weather()


    def get_current_weather(self):
        local_time, tz = utils.get_local_time(self.bs.timezone["id"])
        time_frames = self.bs.find_all("time")
        temperature = []
        wind_direction = []
        wind_speed = []
        percipitation = []
        weather = []
        forecast_time = []
        for i in range(0,self.time_frame_count):
            forecast_time.append(utils.get_time(time_frames[i]['from']))
            forecast_time.append(utils.get_time(time_frames[i]['to']))
            temperature.append(time_frames[i].temperature['value'])
            wind_direction.append(self.translate(time_frames[i].winddirection['code'], "direction"))
            wind_speed.append(time_frames[i].windspeed['mps'])
            percipitation.append(time_frames[i].precipitation['value'])
            weather.append(self.translate(time_frames[i].symbol['number'], "weather"))

        self.get_forecast_string(i, forecast_time, temperature, wind_direction, wind_speed, percipitation, weather)


    def translate(self, id, table):
        file_dict = {"weather":'weather_translation_yrno.csv', "direction":"direction_translation_yrno.csv"}
        with open(file_dict[table], mode='r') as infile:
            reader = csv.DictReader(infile, delimiter="\t")
            for row in reader: 
                if row['ID'] == str(id):
                    print(row[self.language])
                    return row[self.language]


    def get_forecast_string(self, i, forecast_time, temperature, wind_direction, wind_speed, percipitation, weather):
        if self.language == "portuguese":
    		self.forecast_string = "Bom dia, são " + time + " este é o tempo para o Curral das Freiras nesta linda manhã " + date + " " + \
            todayDayPart + "," + todaySummary + " a temperatura atual é " + currentTemperture + " será sentido ao longo do dia uma temperatura máxima de " + high + ", e uma temperatura mínima de " + low +  " espero que continuem connosco. Tenha uma boa manhã."
        
        elif self.language == "romanian":
             self.forecast_string = "Bună ziua Sfântu Gheorghe. Prognoza pentru ora " + forecast_time[0] + \
                " până la ora " + forecast_time[1] + " azi este astăzi înnorat, cu o temperatură de " + temperature[0] + \
                " grade, cu vânt de " + wind_speed[0] + " metri pe secundă din direcția est. Prognoza de astăzi la ora " + \
                forecast_time[2] + " până la ora " + forecast_time[3] + " PM este înnorat, cu o temperatură de " + temperature[1] + \
                " grade, cu vânt de " + wind_speed[1] + "metri pe secundă din direcția " + wind_direction[1] + \
                ". Prognoza meteo din Yr, livrată de Institutul Meteorologic din Norvegia și NRK."

        elif self.language == "english":
            self.forecast_string = "Hello, it is currently " + time + "in " + getStationLocation(station) + "." + "The forecast for " + timeFrame + \
                "The forcast for " + timeframe + " is " + weather + " and " + temperature + " degrees, with wind of " + wind_speed + \
                " meters per second, in the " + wind_direction + " direction."
        
        else:
            self.forecast_string = ""


def main():
    # parser = argparse.ArgumentParser(description='Generates wav file based on current forecast on tempo.pt')
    # parser.add_argument('station', type=str, help='station location code (cu, ma)')
    # parser.add_argument('accent', type=str, help='PT accent code (pt, br, md)')
    # parser.add_argument('-g', '--gender', type=str, default="female", help='Preferred gender of speaker)')
    # args = parser.parse_args()
    forecast = YrForecast("cu", "romanian")
    forecast_string = forecast.create_forecast_string()
    print(forecast_string)
    utils.get_cprc_tts(forecast.forecast_string, "romanian", "female", accent=None, strict_gender=False, \
        strict_accent=False, sample_rate=8000, audio_format='wav', metadata=True)
        

if __name__ == "__main__":
    main()  