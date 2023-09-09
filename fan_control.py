#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
import os
import sys

from datetime import datetime


def clamp(minn, n, maxn):
    return sorted([minn, n, maxn])[1]

def strtobool(value):
    _MAP = {
        'y': True,
        'yes': True,
        't': True,
        'true': True,
        'on': True,
        '1': True,
        'n': False,
        'no': False,
        'f': False,
        'false': False,
        'off': False,
        '0': False
    }
    try:
        return _MAP[str(value).lower()]
    except KeyError:
        raise ValueError('"{}" is not a valid bool value'.format(value))

# Globals / Consts
logging_enabled = strtobool( os.getenv('LOGGING_ENABLED', 'False') )

gpio_pwm_pin = int( os.getenv('GPIO_PWM_PIN', 12) )
invert_pwm_signal = strtobool( os.getenv('INVERT_PWM_SIGNAL', 'False') )

cpu_temp_threshold_degrees = float( os.getenv('CPU_TEMP_THRESHOLD_DEGREES', 54) )
update_interval_sec = clamp( 0.5, float( os.getenv('UPDATE_INTERVAL_SEC', 1.5) ), 60 )
cooldown_factor = clamp( 1, int( os.getenv('COOLDOWN_FACTOR', 5) ), 1000 )  # How long the fan should continue spinning before slowing down (= COOLDOWN_FACTOR x UPDATE_INTERVAL_SEC)

dc_min = clamp( 0, float( os.getenv('DC_MIN', 0) ), 100 )
dc_max = clamp( dc_min, float( os.getenv('DC_MAX', 100) ), 100 )

DC_INIT = 0          # WHEN STARTING APP: FAN OFF
DC_STEP = 5


# --- Functions
def init_pwm(pwm_pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(pwm_pin, GPIO.OUT)
    return GPIO.PWM(pwm_pin, 50)

def read_cpu_temp():
    tmp = os.popen('vcgencmd measure_temp').readline()
    return float( (tmp.replace("temp=","").replace("'C\n","")) )

def create_set_pwm_dc(pwm):
    def set_pwm_dc(dc_next):
        dc_applied = 0 if dc_next == 0 else clamp(dc_min, dc_next, dc_max)
        pwm.ChangeDutyCycle( dc_applied if not invert_pwm_signal else 100 - dc_applied )
        return dc_next, dc_applied
    return set_pwm_dc


if __name__ == "__main__":
    print(f"Running as user '{os.path.split(os.path.expanduser('~'))[-1]}' on '{os.uname()[1]}'")
    print(f"{logging_enabled=} {gpio_pwm_pin=} {invert_pwm_signal=} {DC_INIT=} {DC_STEP=} {dc_min=} {dc_max=} {cpu_temp_threshold_degrees=} {update_interval_sec=}")
    print("\n")

    try:
        pwm = init_pwm( gpio_pwm_pin )
        set_pwm_dc = create_set_pwm_dc(pwm)

        dc_cur = dc_applied = DC_INIT
        pwm.start( dc_cur if not invert_pwm_signal else 100 - dc_cur )

        cool_down = 0
        while True:
            cpu_temp = read_cpu_temp()

            if (cpu_temp > cpu_temp_threshold_degrees):         # fanUp
                if dc_cur < 100:
                    dc_cur, dc_applied = set_pwm_dc( dc_cur + DC_STEP )
                cool_down = cooldown_factor -1
            elif (cpu_temp < cpu_temp_threshold_degrees):       # fanDown
                if cool_down == 0:
                    if dc_cur > 0:
                        dc_cur, dc_applied = set_pwm_dc( dc_cur - DC_STEP )
                else:
                    cool_down -= 1

            if logging_enabled:
                print('%s --- Current temp: %f ℃, dutycycle: %f (applied: %f), cooldown: %d' % (datetime.now().astimezone().isoformat(timespec='seconds'), cpu_temp, dc_cur, dc_applied, cool_down))

            sleep(update_interval_sec)

    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
