# -*- coding: UTF-8 -*
import requests
import datetime
from cereproc.cerecloud_rest import CereprocRestAgent
from suds.client import Client
import ConfigParser
import pytz


def get_cprc_tts(text, language='english', gender='female',  accent=None, strict_gender=False, \
				 strict_accent=False, sample_rate='8000', audio_format='wav', metadata=True):
		file = "weather/audio/"+ datetime.datetime.now().strftime("%Y%m%d%H%M")
		# config = configparser.ConfigParser()
		# config.read('config.ini')
		# username = config['cerecloud']['CEREPROC_USERNAME']
		# password = config['cerecloud']['CEREPROC_PASSWORD']
		username = "5aec2e36c429d"
		password = "VkZmL42e5L"
		print(file)
		restAgent = CereprocRestAgent("https://cerevoice.com/rest/rest_1_1.php", username, password, gender, language)
		voice = restAgent._choose_voice(language, gender, accent, strict_gender, strict_accent)
		url, transcript = restAgent.get_cprc_tts(text, voice, sample_rate, audio_format, metadata)
		r = requests.get(url)
		with open(file + ".wav", 'wb') as f:
				f.write(r.content)
		with open(file + ".txt", 'wb') as f:
				f.write(text)


def get_cprc_tts_soap():
		username = "5aec2e36c429d"
		password = "VkZmL42e5L"
		## SOAP Client
		soapclient = Client("https://cerevoice.com/soap/soap_1_1.php?WSDL")
		xml = """<speak version="1.0" 
      xmlns="http://www.w3.org/2001/10/synthesis" 
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.w3.org/2001/10/synthesis
        http://www.w3.org/TR/speech-synthesis/synthesis.xsd"
      xmlns:myssml="http://www.example.com/ssml_extensions"
      xmlns:claws="http://www.example.com/claws7tags"
      xml:lang="en">&lt;prosody rate='x-slow'&gt;testing&lt;/prosody&gt;</speak>"""
		
		#xml = open("input.xml", "r").read()
		
		request = soapclient.service.speakExtended(username, password, 'Lucia', xml)
		print(request)


def getHTML(feed):
		response = requests.get(feed)
		response.raise_for_status() #if error it will stop the program
		response = response.content
		HTMLFeed = BeautifulSoup(response, 'html.parser')
		return HTMLFeed

 # update to use actual file name. take paramaters for indicating which date it is about. 
 # decide on date file format - use the config file, have variables named based on the parameters
def getLastDate():
    if os.path.exists(dateFile):
        file = open(dateFile, "r") 
        lastDate = file.read() 
        file.close()
        try:
            return datetime.datetime.fromtimestamp(int(lastDate))
        except:
            return datetime.datetime.fromtimestamp(int(0))
            
    else:
        return datetime.datetime.fromtimestamp(0)


def setLastDate(lastDate):   
    if os.path.exists(dateFile):
        f = open(dateFile, "w")
        f.write(str(lastDate))
        f.close()


def get_local_time(time_zone):
	tz = pytz.timezone(time_zone)
	local_time = datetime.datetime.now(tz)
	return(local_time, tz)


def day_part(time_zone):
	tz = pytz.timezone(time_zone)
	local_time = datetime.datetime.now(tz)
	if local_time.hour < 4:
		return 2
	elif local_time.hour < 12:
	    return 0
	elif 12 <= local_time.hour < 18:
	    return 1
	else:
	    return 2

def next_index_loop(items, idx):
	if idx >= len(items):
		return(0)
	else:
		return(idx+1)



# Convert time string of a specific formate to time object, return 
def get_time(time_string):
    time = datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
    return(time.strftime("%H:%M"))