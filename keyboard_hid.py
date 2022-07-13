import logging, tty, sys, termios, time, asyncio
from selectors import EpollSelector
from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO

class Keyboard():
    def __init__(self):
        logging.info('Init keyboard')
        self.event = bytearray(8)
        self.event_key_position = 3
        #2^  0 - lctrl, 1 - lshift, 2 - lalt, 4 - rctrl, 5 - rshift, 6- ralt
        self.special_keys = {'leftctrl': 1, 'leftshift': 2, 'leftalt': 4,'rightctrl': 16, 'rightshift': 32,  'rightalt': 64}

    def read_event(self):
        try:
            dev = InputDevice('/dev/input/event1')
            logging.info('Keyboard connected')
            led_light.blinking('ON')
            for event in dev.read_loop():
                if event.type == ecodes.EV_KEY:
                    self.handle_event(str(categorize(event)))
                    # example categorize(event) = 'key event at 1657551596.711892, 28 (KEY_ENTER), up'
        except Exception as e:
            logging.info(f'Keyboard connection failed: {e}')
            led_light.blinking('ERROR')
    
    def handle_event(self, event):
        key = event.split()[-2].lower().partition('_')[2].strip('),') # 'enter'
        status = event.split()[-1] # 'up'
        try:
            if status == 'down':
                self.format_event(key)
            elif status == 'up':
                self.send_msg()
                logging.info('Release keys')
                self.reset_event()
        except Exception as e:
            logging.warning(f'handle_event error: {e}')

    def format_event(self, key):
        # key = 'enter'
        if key in self.special_keys:
            if self.event[0] == 0:
                self.event[0] = self.special_keys[key]
                logging.info(f'Add special key {key}')
            else:
                logging.info(f'Add next special keys {key}!')
                self.event[0] = self.event[0] + self.special_keys[key]
        else:
            logging.info(f'Pressed down {key}')
            self.event[self.event_key_position] = keys[key]
            self.event_key_position += 1
        
    def send_msg(self):
        logging.info(f'SEND {bytes(self.event)}')
        self.write_key(self.event)
        self.release_key()
        self.event = 0

    def write_key(self, report):
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report)

    def release_key(self):
        release_report = (chr(0)*8).encode()
        self.write_key(release_report)

    def reset_event(self):
        self.event_key_position = 3
        self.event = bytearray(8)

class LED():
    def __init__(self) -> None:
        self.connected = False
        logging.info('Init LED')
        self.try_connection()

    def try_connection(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(2,GPIO.OUT)
            GPIO.output(2,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(2,GPIO.LOW)
            self.connected = True
            logging.info('LED connected')
        except Exception as e:
            logging.info(f'LED failed, error: {e}')
            self.connected = False

    def blinking(self, state):
        if self.connected:
            if state == 'ON':
                GPIO.output(2,GPIO.HIGH)

            elif state == 'ERROR':
                for i in range(3):
                    GPIO.output(2,GPIO.LOW)
                    time.sleep(1)
                    GPIO.output(2,GPIO.HIGH)
                    time.sleep(1)
            else:
                logging.info(f'LED other state: {state}')      

async def start():
    logging.info('Starting event loop...')
    while 1:
        keyboard.read_event()

        
if __name__ == '__main__':
    logging.basicConfig(filename='logs.log', filemode='w', format='%(asctime)s:  %(message)s')
    logging.info = logging.warning
    logging.info('Enetring main')

        # mapping keys
    letter_dict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    '1','2', '3', '4', '5', '6', '7', '8', '9', '0']

    _letter_dict_DLC = {'enter': 88, 'esc': 41, 'backspace': 42, 'tab': 43, 'space' : 44, 
            'brightnessdown': 58, 'brightnessup': 59, 'scale': 60, 'dashboard': 61, 'kbdillumdown': 62, 'kbdillumup': 63,
             'previoussong': 64, 'playpause': 65, 'nextsong': 66, "mute']": 67, 'volumedown': 68, 'volumeup': 69, 'delete': 76, #f9-f12 to do
            'right': 79, 'left': 80, 'down': 81, 'up': 82,}

    # letter_code = lambda x: chr(0)*2+chr(x)+chr(0)*5
    number = [i + 4 for i in range(len(letter_dict))]
    keys =  dict(zip(letter_dict,number))
    for key, value in _letter_dict_DLC.items():
        _letter_dict_DLC[key] = value
    keys = {**keys, **_letter_dict_DLC}
    
    keyboard = Keyboard()
    led_light = LED()

    asyncio.run(start())
