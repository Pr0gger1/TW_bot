import time
import schedule

def send_forecast(city):
    pass

def loop(time):
    schedule.every().day.at(time).do(send_forecast)
