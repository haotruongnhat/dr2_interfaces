from msilib.schema import Control
import pyvjoy
import time
#Pythonic API, item-at-a-time
from tqdm import tqdm
import numpy as np
import keyboard
import pyttsx3

MIN_VALUE = 0
MAX_VALUE = 32768
NUM_BUTTONS = 15
LBUTTONS_MAPPING = np.power(2, np.arange(NUM_BUTTONS), dtype=np.int64)

class Controller(pyvjoy.VJoyDevice):
    def __init__(self, vjoy_id = 1):
        super().__init__(vjoy_id)
        self.reset_all()

    def reset_all(self):
        self.reset()
        self.reset_data()
        self.reset_buttons()
        self.reset_povs()

        self.data.wAxisX = MIN_VALUE 
        self.data.wAxisY = MIN_VALUE 
        self.data.wAxisZ = MIN_VALUE
        self.data.wAxisXRot = MIN_VALUE 
        self.data.wAxisYRot = MIN_VALUE 
        self.data.wAxisZRot = MIN_VALUE
        self.data.wSlider = MIN_VALUE
        self.data.wDial = MIN_VALUE

    def testing(self):
        print("Testing Slider")
        for i in tqdm(np.linspace(MIN_VALUE, MAX_VALUE, num=20, dtype=np.int64)):
            self.data.wAxisX = i 
            self.data.wAxisY = i 
            self.data.wAxisZ = i
            self.data.wAxisXRot = i 
            self.data.wAxisYRot = i 
            self.data.wAxisZRot = i
            self.data.wSlider = i
            self.data.wDial = i

            self.update()
            time.sleep(0.1)
        
        buttons = np.zeros(NUM_BUTTONS, dtype= np.int64)
        for i in range(NUM_BUTTONS):
            buttons[i] = 1
        
            self.data.lButtons = self.convert_buttons_to_lbuttons(buttons)
            self.update()
            time.sleep(0.2)

    def auto_binding(self):
        self.converter = pyttsx3.init()
        # Can be more than 100
        self.converter.setProperty('rate', 150)
        # Set volume 0-1
        self.converter.setProperty('volume', 0.7)

        self.print_and_say("Go to the start of the Setting Input in DR")
        time.sleep(2)

        sleep_time = 2
        small_sleep = 0.05
        
        self.print_and_say("Press Accelerate")
        time.sleep(sleep_time)

        self.data.wSlider = MAX_VALUE
        self.update()
        time.sleep(small_sleep)
        self.data.wSlider = MIN_VALUE
        self.update()

        self.print_and_say("Press Brake")

        time.sleep(sleep_time)
        self.data.wDial = MAX_VALUE
        self.update()
        time.sleep(small_sleep)

        self.data.wDial = MIN_VALUE
        self.update()

        self.print_and_say("Press Steer Left")
        time.sleep(sleep_time)

        self.data.wAxisX = MAX_VALUE
        self.update()
        time.sleep(small_sleep)

        self.data.wAxisX = MIN_VALUE
        self.update()

        self.print_and_say("Press Steer Right")
        time.sleep(sleep_time)

        self.data.wAxisY = MAX_VALUE
        self.update()

        time.sleep(small_sleep)

        self.data.wAxisY = MIN_VALUE
        self.update()

        self.print_and_say("Press Handbrake")
        time.sleep(sleep_time)

        self.data.wAxisZ = MAX_VALUE
        self.update()

        time.sleep(small_sleep)

        self.data.wAxisZ = MIN_VALUE
        self.update()

        self.reset_buttons()
        self.update()
        self.print_and_say("Press Pause")
        time.sleep(sleep_time)

        self.clicking_button(4)

        self.print_and_say("Press Recover Vehicle")
        time.sleep(sleep_time)
        self.clicking_button(2)

        self.print_and_say("Press Roadside Repair")
        time.sleep(sleep_time)
        self.clicking_button(3)

        self.print_and_say("Press Gear Up")
        time.sleep(sleep_time*2)

        self.clicking_button(0)

        self.print_and_say("Press Gear Down")
        time.sleep(sleep_time)

        self.clicking_button(1)

        self.print_and_say("Press Menu-Start")
        time.sleep(sleep_time*3)

        self.clicking_button(5)

        self.print_and_say("Press Menu-Navigate Select")
        time.sleep(sleep_time)

        self.clicking_button(6)

        self.print_and_say("Press Menu-Navigate Back")
        time.sleep(sleep_time)

        self.clicking_button(7)

        self.print_and_say("Press Menu-Navigate Up")
        time.sleep(sleep_time)

        self.clicking_button(8)

        self.print_and_say("Press Menu-Navigate Down")
        time.sleep(sleep_time)

        self.clicking_button(9)

        self.reset_all()


    def print_and_say(self, text):
        print(text)
        self.converter.say(text)
        self.converter.runAndWait()

    def convert_buttons_to_lbuttons(self, buttons):
        return np.sum(LBUTTONS_MAPPING*buttons)

    def change_button_state(self, index, value = 1):
        buttons = np.zeros(NUM_BUTTONS, dtype= np.int64)
        buttons[index] = value

        self.data.lButtons = self.convert_buttons_to_lbuttons(buttons)

    def clicking_button(self, index):
        self.change_button_state(index)
        controller.update()
        time.sleep(0.1)
        controller.change_button_state(index, 0)
        controller.update()

    def control_aao(self, steering, throttle, brake, hand_brake, gear_up, gear_down):
        """ Control AAO (All at Once)
        """
        self.data.lButtons = 19 # buttons number 1,2 and 5 (1+2+16)
        self.data.wAxisX = 0x2000
        self.data.wAxisY= 0x7500

        #send data to vJoy device
        self.update()

if __name__ == "__main__":
    controller = Controller()
    # controller.testing()
    controller.reset_all()
    
    # controller.auto_binding()

    ## Catching input from users
    while True:  # making a loop
        if keyboard.is_pressed('1'):  # if key 'q' is pressed
            controller.clicking_button(0)
                
        if keyboard.is_pressed('2'):  # if key 'q' is pressed 
            controller.clicking_button(1)
                
        if keyboard.is_pressed('3'):  # if key 'q' is pressed 
            controller.clicking_button(2)
                
        if keyboard.is_pressed('4'):  # if key 'q' is pressed 
            controller.clicking_button(3)
        
        if keyboard.is_pressed('5'):  # if key 'q' is pressed 
            controller.clicking_button(4)

        if keyboard.is_pressed('6'):  # if key 'q' is pressed 
            controller.clicking_button(5)

        if keyboard.is_pressed('7'):  # if key 'q' is pressed 
            controller.clicking_button(6)

        if keyboard.is_pressed('8'):  # if key 'q' is pressed 
            controller.clicking_button(7)

        if keyboard.is_pressed('9'):  # if key 'q' is pressed 
            controller.clicking_button(8)

        if keyboard.is_pressed('0'):  # if key 'q' is pressed 
            controller.clicking_button(9)

        ## X-axis
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            controller.data.wAxisX = MAX_VALUE
        if keyboard.is_pressed('w'):  # if key 'q' is pressed
            controller.data.wAxisX = MIN_VALUE
        
        ## Y-axis
        if keyboard.is_pressed('e'):  # if key 'q' is pressed
            controller.data.wAxisY = MAX_VALUE
        if keyboard.is_pressed('r'):  # if key 'q' is pressed
            controller.data.wAxisY = MIN_VALUE

        ## Z-axis
        if keyboard.is_pressed('a'):  # if key 'q' is pressed
            controller.data.wAxisZ = MAX_VALUE
        if keyboard.is_pressed('s'):  # if key 'q' is pressed
            controller.data.wAxisZ = MIN_VALUE

        ## XRot-axis
        if keyboard.is_pressed('d'):  # if key 'q' is pressed
            controller.data.wAxisXRot = MAX_VALUE
        if keyboard.is_pressed('f'):  # if key 'q' is pressed
            controller.data.wAxisXRot = MIN_VALUE

        ## XRot-axis
        if keyboard.is_pressed('z'):  # if key 'q' is pressed
            controller.data.wAxisYRot = MAX_VALUE
        if keyboard.is_pressed('x'):  # if key 'q' is pressed
            controller.data.wAxisYRot = MIN_VALUE

        ## XRot-axis
        if keyboard.is_pressed('c'):  # if key 'q' is pressed
            controller.data.wAxisZRot = MAX_VALUE
        if keyboard.is_pressed('v'):  # if key 'q' is pressed
            controller.data.wAxisZRot = MIN_VALUE

        ## XRot-axis
        if keyboard.is_pressed('g'):  # if key 'q' is pressed
            controller.data.wSlider = MAX_VALUE
        if keyboard.is_pressed('h'):  # if key 'q' is pressed
            controller.data.wSlider = MIN_VALUE

        ## XRot-axis
        if keyboard.is_pressed('b'):  # if key 'q' is pressed
            controller.data.wDial = MAX_VALUE
        if keyboard.is_pressed('n'):  # if key 'q' is pressed
            controller.data.wDial = MIN_VALUE

        controller.update()
        time.sleep(0.05)
