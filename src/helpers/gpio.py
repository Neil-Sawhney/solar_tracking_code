import hardware_config as cfg
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(cfg.contract_actuator_pin, GPIO.OUT)
GPIO.setup(cfg.expand_actuator_pin, GPIO.OUT)


def expand_actuator(bool):
    GPIO.output(cfg.expand_actuator_pin, bool)
    GPIO.output(cfg.contract_actuator_pin, not bool)


def contract_actuator(bool):
    GPIO.output(cfg.contract_actuator_pin, bool)
    GPIO.output(cfg.expand_actuator_pin, not bool)
