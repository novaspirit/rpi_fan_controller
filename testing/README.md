
"Updated" version which uses HW PWM w/ the following pros:
  - Less CPU utilization
  - Runs on Ubuntu Server

Installation (on Ubuntu):
  - `pip install rpi-hardware-pwm`
  - Add overlay 2 enable HW pwm as explained [here](https://pypi.org/project/rpi-hardware-pwm/)
  - copy script to `/usr/local/bin`
  - adapt `User` in service file & copy it to `/etc/systemd/system/`
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable fan_control`
