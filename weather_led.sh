#!/bin/sh

### BEGI INIT INFO
# Provides:		WeatherLed
# Required-Start:	$local_fs $network
# Required-Stop:	#local_fs
# Default-Start:	2 3 4 5
# Default-Stop: 	0 1 6
# Short-Description:	WeatherLed
#Description:		Weather Notifing LED For The Raspberry Pi

sleep 1
cd /home/michael/weather
sudo screen -dmS weather_led python3 /home/michael/weather/weather_led.py
