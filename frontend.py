#!/usr/bin/env python3

#         Python Stream Deck Library
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

# Example script showing basic library usage - updating key images with new
# tiles generated at runtime, and responding to button state change events.

import os, threading, socket, json

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")


# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, font_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 26)
    draw.text((image.width / 2, image.height / 2), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)


# Returns styling information for a key based on its position and state.
def get_key_style(deck, key, state):
    # Last button in the example application is the exit button.
    exit_key_index = deck.key_count() - 1

    if key == 1:
        name = "55"
        icon = "55_on.png" if state else "55_off.png"
        font = "Roboto-Regular.ttf"
        label = ""
    elif key == 2:
        name = "70"
        icon = "70_on.png" if state else "70_off.png"
        font = "Roboto-Regular.ttf"
        label = ""
    elif key == 3:
        name = "85"
        icon = "85_on.png" if state else "85_off.png"
        font = "Roboto-Regular.ttf"
        label = ""
    elif key == 4:
        name = "sifa"
        icon = "sifa_on.png" if state else "sifa_off.png"
        font = "Roboto-Regular.ttf"
        label = ""
    elif key == 6:
        name = "bef40"
        icon = "bef40_on.png" if state else "bef40_off.png"
        font = "Roboto-Regular.ttf"
        label = ""
    elif key == 7:
        name = "500"
        icon = "500_on.png" if state else "500_off.png"
        font = "Roboto-Regular.ttf"
        label = ""
    elif key == 8:
        name = "1000"
        icon = "1000_on.png" if state else "1000_off.png"
        font = "Roboto-Regular.ttf"
        label = ""
    elif key == 9:
        name = "T"
        icon = "t_on.png" if state else "t_off.png"
        font = "Roboto-Regular.ttf"
        label = ""
    elif key == 12:
        name = "speed"
        icon = "null.png"
        font = "Roboto-Regular.ttf"
        label = ' ' + str(state).rjust(3, '0') + '\nkm/h'
    else: return {
        "name": "null",
        "icon": os.path.join(ASSETS_PATH, "null.png"),
        "font": os.path.join(ASSETS_PATH, "Roboto-Regular.ttf"),
        "label": ""
    }

    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }


# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.
def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)

def grab_update_key(deck):
    with socket.create_connection((socket.gethostname(), 22223)) as sock:
        while True:
            message = json.loads(sock.recv(65535).decode("utf-8"))
            try:
                if message['55'] == 1: update_key_image(deck, 1, True)
                elif message['55'] == 0: update_key_image(deck, 1, False)
            except KeyError: pass

            try:
                if message['70'] == 1: update_key_image(deck, 2, True)
                elif message['70'] == 0: update_key_image(deck, 2, False)
            except KeyError: pass

            try:
                if message['85'] == 1: update_key_image(deck, 3, True)
                elif message['85'] == 0: update_key_image(deck, 3, False)
            except KeyError: pass
            
            try:
                if message['40'] == 1: update_key_image(deck, 6, True)
                elif message['40'] == 0: update_key_image(deck, 6, False)
            except KeyError: pass

            try:
                if message['500'] == 1: update_key_image(deck, 7, True)
                elif message['500'] == 0: update_key_image(deck, 7, False)
            except KeyError: pass

            try:
                if message['1000'] == 1: update_key_image(deck, 8, True)
                elif message['1000'] == 0: update_key_image(deck, 8, False)
            except KeyError: pass

            try:
                if message['1000'] == 1: update_key_image(deck, 8, True)
                elif message['1000'] == 0: update_key_image(deck, 8, False)
            except KeyError: pass

            try:
                if message['sifawarn'] >= 1: update_key_image(deck, 4, True)
                elif message['sifawarn'] == 0: update_key_image(deck, 4, False)
            except KeyError: pass

            try:
                if message['doorlock'] == 1: update_key_image(deck, 9, False)
                elif message['doorlock'] < 1: update_key_image(deck, 9, True)
            except KeyError: pass

            try: update_key_image(deck, 12, int(message['SpeedometerKPH']))
            except KeyError: pass

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    print(f"Found {len(streamdecks)} Stream Deck(s).\n")

    for index, deck in enumerate(streamdecks):
        # This example only works with devices that have screens.
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print(f"Opened '{deck.deck_type()}' device (serial number: '{deck.get_serial_number()}', fw: '{deck.get_firmware_version()}')")

        # Set initial screen brightness to 30%.
        deck.set_brightness(100)

        # Set initial key images.
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        threading.Thread(target=grab_update_key, args=[deck]).start()

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass