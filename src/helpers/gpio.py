import time

import RPi.GPIO as GPIO

import src.helpers.hardware_config as cfg

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(cfg.contract_actuator_pin, GPIO.OUT)
GPIO.setup(cfg.expand_actuator_pin, GPIO.OUT)


def expand_actuator(milliseconds):
    GPIO.output(cfg.expand_actuator_pin, 1)
    GPIO.output(cfg.contract_actuator_pin, 0)
    time.sleep(milliseconds / 1000)
    GPIO.output(cfg.expand_actuator_pin, 0)
    GPIO.output(cfg.contract_actuator_pin, 0)


def contract_actuator(milliseconds):
    GPIO.output(cfg.expand_actuator_pin, 0)
    GPIO.output(cfg.contract_actuator_pin, 1)
    time.sleep(milliseconds / 1000)
    GPIO.output(cfg.expand_actuator_pin, 0)
    GPIO.output(cfg.contract_actuator_pin, 0)


def home_actuator():
    expand_actuator(10e3)
