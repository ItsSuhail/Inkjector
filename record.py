import sys 
import pickle
import pyautogui
from pynput import *
import time


coordinates_list = []
x_coordinates = []
y_coordinates = []

def serialize(entry, entry_coordinates_list, min_coordinates, max_coordinates):
    data = {}
    try:
        aachar = open("data.pkl", "rb")
        data = pickle.load(aachar)
        aachar.close()
    except FileNotFoundError:
        pass
    except EOFError:
        pass
    data[entry] = {"coordinates":entry_coordinates_list, "min":min_coordinates, "max":max_coordinates}
    aachar = open("data.pkl", "wb")
    pickle.dump(data, aachar)
    aachar.close()



ready = False
held = False

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


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("READY TO RECORD\n")

with mouse.Listener(on_click=on_click) as listener:
    while listener.running:
        if held:
            position = mouse.Controller().position
            if position not in coordinates_list:
                coordinates_list.append(position)
                x_coordinates.append(position[0])
                y_coordinates.append(position[1])

print("RECORDED\n")

entry = input("Name of entry: ")
serialize(entry, coordinates_list, (min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates)))

print("Successfully stored the coordinates\n\n\n")

print(coordinates_list)

# time.sleep(10)
# pyautogui.mouseDown(button="left")
# for coords in coordinates:
#     pyautogui.moveTo(coords[0], coords[1])
# pyautogui.mouseUp(button="left")