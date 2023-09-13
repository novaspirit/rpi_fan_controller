# RPi Fan Control (RPiFC)

Python based script for controlling fan speed on Raspberry Pi via pwm.

https://www.youtube.com/watch?v=lD7t-IGLjVM


---
This is an "updated" version which **uses HW PWM** (the [original implementation](attic/) uses SW PWM; for more details, [see here](https://raspberrypi.stackexchange.com/a/100644))

This allows for a higher frequency while keeping the CPU usage low.

However, the setup is a bit more complex:
  - [Enable](https://pypi.org/project/rpi-hardware-pwm/) HW pwm  (add `dtoverlay=pwm-2chan` in firmware config file)
  - When not using Raspberry Pi OS: Setup permissions via [udev rules](https://github.com/dotnet/iot/blob/main/Documentation/raspi-pwm.md#adding-your-user-to-the-right-permission-group)
  - Install dependencies: `pip install -r requirements.txt`
  - Copy script to `/usr/local/bin`
  - Adapt `User` in service file & copy it to `/etc/systemd/system/`
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable fan_control`
