# Keyboard HID as USB OTG

Python script to make your raspberry pi zero acts like a keyboard \
To raspberry connect via bluetooth keyboard, and plug usb cable into USB OTG port \
In this example was used keyboard Keychron k10\
Also you can connect led (in this project is one led at GPIO 2) \
it blinks while connecting and turn on after succes 


## Authors

- [@Cwalina Piotr](https://github.com/veNNNx)


## Deployment
Run raspberry with plugged usb cable into PWR port. 
Connect via ssh

Clone repo


```bash
  git clone https://github.com/veNNNx/Keyboard_hid_python
```

Run init script
```bash
  cd Keyboard_hid_python
  chmod +x init.sh
  sudo ./init.sh
```

Change USB PWR port to USB OTG 

log file at ~/Keyboard_hid_python/logs.log

## Features

- Make script as daemon service
- Faster raspberry boot
