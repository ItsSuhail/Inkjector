import sys 
import pickle
import pyautogui
from pynput import *
import time


coordinates_list = []
x_coordinates = []
y_coordinates = []

ready = False
held = False


def serialize(entry, entry_coordinates_list, min_coordinates, max_coordinates):
    data = {}
    try:
        achaar = open("data.pkl", "rb")
        data = pickle.load(achaar)
        achaar.close()
    except FileNotFoundError:
        pass
    except EOFError:
        pass
    data[entry] = {"coordinates":entry_coordinates_list, "min":min_coordinates, "max":max_coordinates}
    achaar = open("data.pkl", "wb")
    pickle.dump(data, achaar)
    achaar.close()



def on_press(key):
    global ready
    if key == keyboard.Key.space:
        ready = True

def on_release(key):
    if ready:
        return False

def on_click(x,y, button, pressed):
    global ready, held

    if pressed and ready:
        held = True

    if not pressed and ready:
        ready = False
        held = False
        return False

is_accepted = False

while(not is_accepted):
    coordinates_list = []
    x_coordinates = []
    y_coordinates = []

    ready = False
    held = False

    print("PRESS SPACE TO GET READY: ")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("\nREADY TO RECORD\n")

    with mouse.Listener(on_click=on_click) as listener:
        while listener.running:
            if held:
                position = mouse.Controller().position
                if position not in coordinates_list:
                    coordinates_list.append(position)
                    x_coordinates.append(position[0])
                    y_coordinates.append(position[1])

    print("RECORDED\n")

    min_x, min_y, max_x, max_y = min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)

    relative_coordinates_list = []

    for coordinates in coordinates_list:
        relative_coordinates_list.append((coordinates[0] - min_x, coordinates[1] - min_y))

    max_x = max_x - min_x
    max_y = max_y - min_y
    min_x, min_y = 0, 0

    accepted = input("Accept the recording: ")
    if accepted in ['Y', 'y', 'yes']:
        is_accepted = True
        entry = input("Name of entry: ")
        serialize(entry, relative_coordinates_list, (min_x, min_y), (max_x, max_y))

        print("\nSuccessfully stored the coordinates\n")
        sys.exit()
    elif accepted == "-1":
        sys.exit()
    print("\n\n")