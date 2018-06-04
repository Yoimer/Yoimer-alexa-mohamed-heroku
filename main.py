import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

######################################
from flask import Flask

import json

import requests

######################################


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch

def launch_app():

    welcome_msg = render_template('welcome')

    return statement(welcome_msg)

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


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')



# import logging

# from random import randint

# from flask import Flask, render_template

# from flask_ask import Ask, statement, question, session


# app = Flask(__name__)

# ask = Ask(app, "/")

# logging.getLogger("flask_ask").setLevel(logging.DEBUG)


# @ask.launch

# def new_game():

#     welcome_msg = render_template('welcome')

#     return question(welcome_msg)


# @ask.intent("YesIntent")

# def next_round():

#     numbers = [randint(0, 9) for _ in range(3)]

#     round_msg = render_template('round', numbers=numbers)

#     session.attributes['numbers'] = numbers[::-1]  # reverse

#     return question(round_msg)


# @ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

# def answer(first, second, third):

#     winning_numbers = session.attributes['numbers']

#     if [first, second, third] == winning_numbers:

#         msg = render_template('win')

#     else:

#         msg = render_template('lose')

#     return statement(msg)

# if __name__ == '__main__':

#     app.run(debug=True, host='0.0.0.0')











# import logging

# from random import randint

# from flask import Flask, render_template

# from flask_ask import Ask, statement, question, session

# ######################################
# from flask import Flask

# import json

# import requests

# ######################################


# app = Flask(__name__)

# ask = Ask(app, "/")

# logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# @ask.launch

# def launch_app():

#     welcome_msg = render_template('welcome')

#     return statement(welcome_msg)

# @ask.intent("TemperatureIntent")

# def get_temperature():
#     sess = requests.Session()

#     url = 'https://phpcourse.000webhostapp.com/temperature.txt'

#     data = sess.get(url)
     
#     print data.content
     
#     print "next line is temperature"
    
#     temperature_msg = "Temperature value is: " + data.content + " Celsius degrees"

#     #return statement(data.content)
#     return statement(temperature_msg)

# @ask.intent("HumidityIntent")

# def get_humidity():
#     sess = requests.Session()

#     url = 'https://phpcourse.000webhostapp.com/humidity.txt'

#     data = sess.get(url)
     
#     print data.content
     
#     print "next line is humidity"
    
#     humidity_msg = "Humidity value is: " + data.content + " Percentage"

#     #return statement(data.content)
#     return statement(humidity_msg)


# if __name__ == '__main__':

#     app.run(debug=True, host='0.0.0.0')