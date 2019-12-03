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

    def __init__(self, station, language, gender="female", accent=None, strict_gender=False, \
            strict_accent=False, sample_rate=8000, audio_format='wav', metadata=True, time_frame_count=2):
        self.station = station
        self.language = language
        self.accent = accent
        self.gender = gender
        self.strict_gender = strict_gender
        self.strict_accent = strict_accent
        self.sample_rate = sample_rate
        self.audio_format = audio_format
        self.metadata = metadata
        self.time_frame_count = time_frame_count
        self.generate_forecast_string()
        self.generate_forecast_audio()


    def generate_forecast_string(self):
        url = self.set_yr_URL()
        response = requests.get(url)
        html = response.content
        self.bs = BeautifulSoup(html, 'lxml')
        self.request_current_weather()


    def generate_forecast_audio(self):
        self.forecast_audio = utils.get_cprc_tts(self.forecast_string, self.language, self.gender, self.accent, self.strict_gender, \
            self.strict_accent, self.sample_rate, self.audio_format, self.metadata)


    def request_current_weather(self):
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

        self.set_forecast_string(i, forecast_time, temperature, wind_direction, wind_speed, percipitation, weather)


    def set_forecast_string(self, i, forecast_time, temperature, wind_direction, wind_speed, percipitation, weather):
        print(wind_speed[1], wind_direction[1])
        if self.language == "portuguese":
    		self.forecast_string = "Bom dia, são " + time + " este é o tempo para o Curral das Freiras nesta linda manhã " + date + " " + \
            todayDayPart + "," + todaySummary + " a temperatura atual é " + currentTemperture + " será sentido ao longo do dia uma temperatura máxima de " + high + ", e uma temperatura mínima de " + low +  " espero que continuem connosco. Tenha uma boa manhã."
        
        elif self.language == "romanian":
            day_parts = [["dimineaţă","dupa amiaza","seară"],["buna dimineata","buna ziua","bună seara"]]   
            self.forecast_string = "Sfântu Gheorghe. Prognoza pentru ora " + forecast_time[0] + \
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


    def translate(self, id, table):
        file_dict = {"weather":'weather_translation_yrno.csv', "direction":"direction_translation_yrno.csv"}
        with open(file_dict[table], mode='r') as infile:
            reader = csv.DictReader(infile, delimiter="\t")
            for row in reader: 
                if row['ID'] == str(id):
                    return row[self.language]


    def set_yr_URL(self):
        if self.station == 'cu':
            url = 'https://www.yr.no/place/Portugal/Madeira/Curral_das_Freiras/forecast.xml'
        elif self.station == 'ro':
            url = 'https://www.yr.no/place/Romania/Tulcea/Sf%C3%A2ntu_Gheorghe/forecast.xml'
        else: url = None
        return url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates wav file based on current forecast on yr.no')
    parser.add_argument('station', type=str, help='station location code (cu, ma)')
    parser.add_argument('language', type=str, help='language')
    parser.add_argument('-g', '--gender', type=str, default='female', help='Preferred gender of speaker)')
    parser.add_argument('-a', '--accent', type=str, default=None, help='Preferred gender of speaker)')
    parser.add_argument('-sg', '--strict_gender', default=False, type=str, help='is preferred gender strict?')
    parser.add_argument('-sa', '--strict_accent', default=False, type=str, help='is preferred accent strict?')
    parser.add_argument('-sr', '--sample_rate', default=8000, type=int, help='sample rate')
    parser.add_argument('-af', '--audio_format', default='wav', type=str, help='is preferred accent strict?')
    parser.add_argument('-m', '--metadata', default=False, type=str, help='metadata true or false')
    parser.add_argument('-t', '--time_frame_count', default=2, type=int, help='number of time frames to forecast')

    args = parser.parse_args()
    forecast = YrForecast(args.station, args.language, args.gender, args.accent, args.strict_gender, \
            args.strict_accent, args.sample_rate, args.audio_format, args.metadata, args.time_frame_count)
