#!/bin/bash

echo -e '\033[43mStarting configuration script!\033[0m'

if [ "$EUID" -ne 0 ]
  then 
  echo -e "\033[0;91mPlease run as root\033[0m"
  exit
fi

echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "Netowrk status: \033[32mconnected\033[0m"
else
    echo -e "Network status: \033[0;91mconnection failed\033[0m, stopping process"
	exit
fi


if [ -f "~/Keyboard_hid_python/start.sh" ]; 
then
    echo -e '\033[0;96mKeyboard HID configuration already exists\033[0m'
	exit
else
    echo -e '\033[32m0. Update packages...\033[0m'
    apt-get update
	apt-get upgrade
fi



echo -e '\033[32m1. Enable modules\033[0m'
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "libcomposite" | sudo tee -a /etc/modules



echo -e '\033[32m2. Create keyboard hid bash script\033[0m'
cd ~/Keyboard_hid_python/
touch start.sh
chmod +x start.sh
echo "#!/bin/bash
trap '' INT
echo 'Keybaord interrupts disabled'
sudo python3 ~/Keyboard_hid_python/keyboard_hid.py
echo 'Keybaord interrupts enabled'
trap - INT" > start.sh



echo -e '\033[32m3. Creating the USB gadget config script\033[0m'
touch /usr/bin/keyboard_hid_gadget_usb
chmod +x /usr/bin/keyboard_hid_gadget_usb
sed -i '/^exit*/i /usr/bin/keyboard_hid_gadget_usb' /etc/rc.local
echo "@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@lxterminal --command='~/Keyboard_hid_python/start.sh'
@xscreensaver -no-splash" > /etc/xdg/lxsession/LXDE-pi/autostart

echo '#!/bin/bash
cd /sys/kernel/config/usb_gadget/
mkdir -p keyboard_hid_gadget
cd keyboard_hid_gadget
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "0123456789" > strings/0x409/serialnumber
echo "Keychron K10" > strings/0x409/manufacturer
echo "Keyboard Ble HID Device" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "Example configuration" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1

ls /sys/class/udc > UDC' > /usr/bin/keyboard_hid_gadget_usb



echo -e '\033[32m4. Installing required packages\033[0m'
apt-get install evtest
apt-get install python3
apt-get install -y python3-evdev



echo -e '\033[32mInstallation finished !!!\033[0m'
echo 'To apply changes reboot raspberry manually'
