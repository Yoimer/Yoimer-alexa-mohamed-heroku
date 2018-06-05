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

##########activate relay##########
# voice commands are:
#Alexa, ask project system to activate relay

# turn system on
@ask.intent("ActivateIntent")

def turn_on():

    sess = requests.Session()

    # read lastest state of button from ubidot
    url = 'http://things.ubidots.com/api/v1.6/devices/alexa/button/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'
     
    data = sess.get(url)

    # data as a dictionary in d
    d = json.loads(data.content)
    # takes the last value saved from nodemcu in ubidots
    d_str = str(d['results'][0]['value'])

    print d_str

    # check whether system is ON already
    if '1.0' in d_str:

        turn_on_msg = "LED is already activated. Not action taken."

        print(turn_on_msg)

        return statement(turn_on_msg)

    #changes states to ON  in ubidot in order to be read by Nodemcu
    else:
        sess = requests.Session()

        # r = requests.post(url, data = data = {'value':1.0})
        requests.post(url, data = {'value':1.0})

        data = sess.get(url)

        # data as a dictionary in d
        d = json.loads(data.content)
        # takes the last value saved from nodemcu in ubidots
        d_str = str(d['results'][0]['value'])

        print d_str

        turn_on_msg = "Turning LED ON... It might take a few seconds, please wait."

        print(turn_on_msg)

        return statement(turn_on_msg)

##########ask for temperature##########
# voice commands are:
#Alexa, ask project system for temperature

# check temperature
@ask.intent("TemperatureIntent")

def get_temperature():
    sess = requests.Session()

    url = 'http://things.ubidots.com/api/v1.6/devices/alexa/temperature/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'

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

# check humidity
@ask.intent("HumidityIntent")

def get_humidity():
    sess = requests.Session()

    url = 'http://things.ubidots.com/api/v1.6/devices/alexa/humidity/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'

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

# check any process variable on system
@ask.intent("FullStatusIntent")

def get_full_status():
    print 'fullstatus...'

    sess = requests.Session()

    #get temperature
    url = 'http://things.ubidots.com/api/v1.6/devices/alexa/temperature/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'

    data = sess.get(url)
    # data as a dictionary in d
    d = json.loads(data.content)
    # takes the last value saved from nodemcu in ubidots and make it a string
    temp_str = str(d['results'][0]['value'])

    #get humidity
    url = 'http://things.ubidots.com/api/v1.6/devices/alexa/humidity/values?token=A1E-Z4kgHL1BHoC5rgQ5sH0Wcey1H8JRf1'

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

                    "temperature say... alexa ask project system for temperature...",

                    "humidity say... alexa ask project system for humidity...",

                    "the whole variable process say... alexa ask project system for full status..."
                ]

    # say a radom msg from help_list
    help_msg = "To ask for " + help_list[random.randint(0,(len(help_list) - 1))]
    reprompt_msg = "...Please" + help_msg
    reprompt_msg += "or. say... stop to close the skill"
    #return statement(help_msg)
    return question(help_msg).reprompt(reprompt_msg)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')