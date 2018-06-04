import logging

import random
#from random import randint
from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

######################################
from flask import Flask

import json

import requests

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


######################################
# Skill name: project
# Invocation Name : project system


##########launch skill##########
# voice commands are:
#Alexa, launch project system

# launch skill
@ask.launch
# read welcome message from template.yaml file
def launch_app():

    welcome_msg = render_template('welcome')

    #return statement(welcome_msg)
    return question(welcome_msg)


##########stop skill##########
# voice commands are:
# stop
#Alexa, stop

# stop skill
#@ask.intent("StopIntent")
@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Stopping the skill, thanks for using")

##########ask for temperature##########
# voice commands are:
#Alexa, ask project system for temperature
#Alexa, give me temperature from project system

# check temperature
@ask.intent("TemperatureIntent")

def get_temperature():
    sess = requests.Session()

    url = 'http://things.ubidots.com/api/v1.6/devices/temperature/temperature/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'

    data = sess.get(url)

    # data as a dictionary in d
    d = json.loads(data.content)
    # takes the last value saved from nodemcu in ubidots
    d_str = str(d['results'][0]['value'])

    temperature_msg = "The temperature value is: " + d_str + " Celsius degrees"

    return statement(temperature_msg)



##########ask for humidity##########
# voice commands are:
#Alexa, ask project system for humidity
#Alexa, give me humidity from project system

# check humidity
@ask.intent("HumidityIntent")

def get_humidity():
    sess = requests.Session()

    url = 'http://things.ubidots.com/api/v1.6/devices/humidity/humidity/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'

    data = sess.get(url)

    # data as a dictionary in d
    d = json.loads(data.content)
    # takes the last value saved from nodemcu in ubidots
    d_str = str(d['results'][0]['value'])

    humidity_msg = "The humidity value is: " + d_str + " Percentage"

    #return statement(data.content)
    return statement(humidity_msg)


##########ask for full process variable status##########
# voice commands are:
#Alexa, ask project system for full status
#Alexa, give me full status from project system

# check any process variable on system
@ask.intent("FullStatusIntent")

def get_full_status():
    print 'fullstatus...'

    sess = requests.Session()

    #get temperature
    url = 'http://things.ubidots.com/api/v1.6/devices/temperature/temperature/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'
    data = sess.get(url)
    # data as a dictionary in d
    d = json.loads(data.content)
    # takes the last value saved from nodemcu in ubidots and make it a string
    temp_str = str(d['results'][0]['value'])

    #get humidity
    url = 'http://things.ubidots.com/api/v1.6/devices/humidity/humidity/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'
    data = sess.get(url)
    # data as a dictionary in d
    d = json.loads(data.content)
    # takes the last value saved from nodemcu in ubidots and make it a string
    humidity_str = str(d['results'][0]['value'])
    #replies both values
    bothvariables_msg = "The temperature value is: " + temp_str + " Celsius degrees" + "..." + " and " + " The humidity value is: " + humidity_str + " Percentage"
    return statement(bothvariables_msg)


##########ask for help##########
# voice commands are:
#help (when welcoming)
#Alexa ask project system for help (anytime)

# ask for help when welcoming or anytime
@ask.intent("AMAZON.HelpIntent")
def help():

    help_list = [

                    "temperature say... alexa give me temperature from project system...",

                    "humidity say... alexa give me humidity from project system...",

                    "the whole variable process say... alexa give me full status from project system..."
                ]

    # say a radom msg from help_list
    help_msg = "To ask for " + help_list[random.randint(0,(len(help_list) - 1))]
    reprompt_msg = "...Please" + help_msg
    reprompt_msg += "or. say... stop to close the skill"
    #return statement(help_msg)
    return question(help_msg).reprompt(reprompt_msg)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')