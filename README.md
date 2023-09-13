# RPi Fan Control (RPiFC)

Python based script for controlling fan speed on Raspberry Pi via pwm.

https://www.youtube.com/watch?v=lD7t-IGLjVM


---
This is an "updated" version which **uses HW PWM** (the [original implementation](attic/sw-pwm/) uses SW PWM; for more details, [see here](https://raspberrypi.stackexchange.com/a/100644))

This allows for a higher PWM frequency (making the fan run smoother) while keeping the CPU usage low.

However, the setup is a bit more involved:
  - Enable HW PWM:
    - [Configure HW PWM](https://pypi.org/project/rpi-hardware-pwm/)  (add `dtoverlay=pwm-2chan` in firmware config file)
    - OPTIONAL (not required on Raspberry Pi OS or when running as root user): Setup permissions via [udev rules](https://github.com/dotnet/iot/blob/main/Documentation/raspi-pwm.md#adding-your-user-to-the-right-permission-group)
    - Reboot
  - Install dependencies: `pip install -r requirements.txt`
  - OPTIONAL: Setup autorun:
    - Copy script to `/usr/local/bin`
    - Adapt `User` in service file & copy it to `/etc/systemd/system/`
    - `sudo systemctl daemon-reload`
    - `sudo systemctl enable fan_control`

Also, hardware pwm [breaks audio apparently](https://forums.raspberrypi.com/viewtopic.php?t=291854).
