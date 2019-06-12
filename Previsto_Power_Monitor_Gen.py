#!/usr/bin/env python3
# Previsto Power Monitor Monitor Gen Version 1.0 - First Release
import RPi.GPIO as GPIO
import time
from datetime import datetime
import http.client
import urllib
import requests

class PrevistoPowerMonitor(object): # The class for the main power monitor program
    def __init__(self, pushover_token, pushover_user, power_off_duration_alert_time, power_off_reminder_time):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # Set up the GPIO ports
        self.power_fail = 24
        GPIO.setup(self.power_fail, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.power_on = False
        self.power_off_duration_alert_time = power_off_duration_alert_time * 3600
        self.power_off_reminder_time = power_off_reminder_time * 3600
        self.long_duration_printed = False
        self.power_off_duration = 0
        # Set up pushover
        self.pushover_token = pushover_token
        self.pushover_user = pushover_user
        
    def print_status(self, print_message):
        today = datetime.now()
        print(print_message + today.strftime('%A %d %B %Y @ %H:%M:%S'))

    def send_pushover_message(self, token, user, pushed_message, alert_sound):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
                        "token": token,
                        "user": user,
                        "html": "1",
                        "title": "Previsto",
                        "message": pushed_message,
                        "sound": alert_sound,
                        }), { "Content-type": "application/x-www-form-urlencoded" })
            
    def shutdown_cleanup(self):
        GPIO.cleanup()
        self.print_status("Previsto Power Monitor Stopped on ")
        
    def run(self):
        startup_state = GPIO.input(self.power_fail)
        if startup_state == True:
            self.print_status("Previsto Power Monitor Started with Power Off on ")
            startup_message = "Previsto Power Monitor Started with Power Off"
            self.power_on = False
            power_off_start = time.time()
        else:
            self.print_status("Previsto Power Monitor Started with Power On on ")
            startup_message = "Previsto Power Monitor Started with Power On"
            self.power_on = True
            power_on_start = time.time()
        self.send_pushover_message(self.pushover_token, self.pushover_user, startup_message, "updown")
        try:
            while True: # Run Power Monitor in continuous loop
                if GPIO.input(self.power_fail) == True: # Check if the power has failed
                    if self.power_on == True: # Send pushover message if the previous power state was on
                        self.print_status("Previsto Power Failed on ")
                        self.send_pushover_message(self.pushover_token, self.pushover_user, "Previsto Power Failed", "updown")
                        self.power_on = False
                        power_off_start = time.time()
                    self.power_off_duration = time.time() - power_off_start
                    if self.power_off_duration > self.power_off_duration_alert_time:
                        if self.long_duration_printed == False:
                            long_power_failure_message = "Previsto Power has been off for " + str(round(self.power_off_duration/3600, 1)) + " hours"
                            self.print_status(long_power_failure_message + " on ")
                            self.send_pushover_message(self.pushover_token, self.pushover_user, long_power_failure_message, "updown")
                            self.long_duration_printed = True
                            self.previous_power_off_reminder_time = time.time()
                        else:
                            if (time.time() - self.previous_power_off_reminder_time >= self.power_off_reminder_time):
                                long_power_failure_message = "Previsto Power has been off for " + str(round(self.power_off_duration/3600, 1)) + " hours"
                                self.print_status(long_power_failure_message + " on ")
                                self.send_pushover_message(self.pushover_token, self.pushover_user, long_power_failure_message, "updown")
                                self.previous_power_off_reminder_time = time.time()
                else:
                    if self.power_on == False:# Send pushover message if the previous power state was off
                        power_on_message = "Previsto Power Restored after being off for " +str(round(self.power_off_duration/60, 0)) + " minutes"
                        self.print_status(power_on_message + " on ")
                        self.send_pushover_message(self.pushover_token, self.pushover_user, power_on_message, "magic")
                        self.power_on = True
                        power_on_start = time.time()
                        self.long_duration_printed = False
                        
                time.sleep(5)
        except KeyboardInterrupt: # Shutdown on ctrl C
            # Shutdown main program
            self.shutdown_cleanup()
            
if __name__ == '__main__': # This is where to overall code kicks off
    monitor = PrevistoPowerMonitor(pushover_token = "<your pushover token>", pushover_user = "<your pushover user>",
                                   power_off_duration_alert_time = 10, power_off_reminder_time = 1)
    monitor.run()
        

