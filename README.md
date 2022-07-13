# Keyboard HID as USB OTG

Python script to make your raspberry pi zero acts like a keyboard \
To raspberry connect via bluetooth keyboard, and plug usb cable into USB OTG port \
In this example was used keyboard Keychron k10


## Authors

- [@Cwalina Piotr](https://github.com/veNNNx)


## Deployment
Run raspberry with plugged usb cable into PWR socket
Run clean raspbian on raspberry and connect to it by ssh
Optional: Connect bluetooth keyboard to raspberry

Clone repo
```bash
  git clone veNNNx/Keyboard_hid_python
```

Run init script
```bash
  cd Keyboard_hid_python
  chmod +x init.sh
  sudo ./init.sh
```
Now you can reboot raspberry and plug usb cable into USB OTG socket
## Features

- Make script as daemon service
- Faster raspberry boot
