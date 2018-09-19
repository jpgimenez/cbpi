# -*- coding: utf-8 -*-
# GPIO Input plugin for Craftbeerpi
# Version 0.1 based on the work of
# https://github.com/mrillies/cbpi_GPIO_input

import time
from modules import cbpi
from modules.core.hardware import SensorActive
from modules.core.props import Property
import requests

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except Exception as e:
    print e
    pass


@cbpi.sensor
class GPIObutton(SensorActive):

    aa_base_url = Property.Text("0. Base URL", configurable=True, default_value="http://127.0.0.1:5000/api", description="Base URL for API")
    ab_debounce =  Property.Number("0. Debounce time", configurable=True, default_value=100, description="Debounce time millis")
    ba_gpio = Property.Select("1. GPIO", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27])
    bb_GETPOST = Property.Select("1. GET or POST", options=["GET", "POST"], description="GET or POST call to API")
    bc_CMD = Property.Text("1. API command", configurable=True, default_value="/step/next", description="API command")
    ca_gpio = Property.Select("2. GPIO", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 99])
    cb_GETPOST = Property.Select("2. GET or POST", options=["GET", "POST", "N/A"], description="GET or POST call to API")
    cc_CMD = Property.Text("2. API command", configurable=True, default_value="/", description="API command")
    da_gpio = Property.Select("3. GPIO", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 99])
    db_GETPOST = Property.Select("3. GET or POST", options=["GET", "POST", "N/A"], description="GET or POST call to API")
    dc_CMD = Property.Text("3. API command", configurable=True, default_value="/", description="API command")
    ea_gpio = Property.Select("4. GPIO", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 99])
    eb_GETPOST = Property.Select("4. GET or POST", options=["GET", "POST", "N/A"], description="GET or POST call to API")
    ec_CMD = Property.Text("4. API command", configurable=True, default_value="/", description="API command")

    def init(self):
        self.data = 0
        self.data_old = 0
        GPIO.setup(int(self.ba_gpio), GPIO.IN , pull_up_down = GPIO.PUD_DOWN)
        GPIO.remove_event_detect(int(self.ba_gpio))
        GPIO.add_event_detect(int(self.ba_gpio), GPIO.BOTH, callback=self.IO_interrupt, bouncetime=self.ab_debounce)
        if int(self.ca_gpio) != 99:
            GPIO.setup(int(self.ca_gpio), GPIO.IN , pull_up_down = GPIO.PUD_DOWN)
            GPIO.remove_event_detect(int(self.ca_gpio))
            GPIO.add_event_detect(int(self.ca_gpio), GPIO.BOTH, callback=self.IO_interrupt, bouncetime=self.ab_debounce)
        if int(self.da_gpio) != 99:
            GPIO.setup(int(self.da_gpio), GPIO.IN , pull_up_down = GPIO.PUD_DOWN)
            GPIO.remove_event_detect(int(self.da_gpio))
            GPIO.add_event_detect(int(self.da_gpio), GPIO.BOTH, callback=self.IO_interrupt, bouncetime=self.ab_debounce)
        if int(self.ea_gpio) != 99:
            GPIO.setup(int(self.ea_gpio), GPIO.IN , pull_up_down = GPIO.PUD_DOWN)
            GPIO.remove_event_detect(int(self.ea_gpio))
            GPIO.add_event_detect(int(self.ea_gpio), GPIO.BOTH, callback=self.IO_interrupt, bouncetime=self.ab_debounce)
        self.api.app.logger.info("GPIO - Init Complete")
        self.data_received(0)

    def get_unit(self):
        unit = "N/A"
        return unit

    def IO_interrupt(self, channel):
        if GPIO.input(channel) == 1:
            method=""
            if int(channel) == int(self.ba_gpio):
                method=self.bb_GETPOST
                url=self.aa_base_url + self.bc_CMD
            if int(channel) == int(self.ca_gpio):
                method=self.cb_GETPOST
                url=self.aa_base_url + self.cc_CMD
            if int(channel) == int(self.da_gpio):
                method=self.db_GETPOST
                url=self.aa_base_url + self.dc_CMD
            if int(channel) == int(self.ea_gpio):
                method=self.eb_GETPOST
                url=self.aa_base_url + self.ec_CMD
            if method != "":
                self.api.app.logger.info("GPIO - IO number - %s - %s %s" % (channel, method, url))
                req = requests.request(method, url)
            self.data = 100
            self.data_old = 1
            self.api.app.logger.info("GPIO - button pushed %s" % (self.data))
        else:
            self.data = 0
            self.data_old = 1
            self.api.app.logger.info("GPIO - button released %s" % (self.data))

    def execute(self):
        while self.is_running():
            self.api.app.logger.info("GPIO - data %s" % (self.data))
            if self.data_old != 0:
                self.data_old = 0
                self.data_received(self.data)
            self.sleep(1)

    def stop(self):
        self.__running = False
        self.api.app.logger.info("GPIO - ge moogt naar huis gaan")
        GPIO.cleanup([int(self.ba_gpio)])
        GPIO.remove_event_detect(int(self.ba_gpio))
        if int(self.ca_gpio) != 99:
            GPIO.cleanup([int(self.ca_gpio)])
            GPIO.remove_event_detect(int(self.ca_gpio))
        if int(self.da_gpio) != 99:
            GPIO.cleanup([int(self.da_gpio)])
            GPIO.remove_event_detect(int(self.da_gpio))
        if int(self.ea_gpio) != 99:
            GPIO.cleanup([int(self.ea_gpio)])
            GPIO.remove_event_detect(int(self.ea_gpio))
