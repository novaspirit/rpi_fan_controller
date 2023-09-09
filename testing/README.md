
"Updated" version which [runs on Ubuntu Server](https://ubuntu.com/tutorials/gpio-on-raspberry-pi#1-overview)

Installation (on Ubuntu):
  - `sudo apt install python3-lgpio`
  - copy script to `/usr/local/bin`
  - copy service to `/etc/systemd/system/`
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable fan_control`
