#!/opt/homebrew/bin/python3

import time
import click
from executor import WindowExecutor
from api import HaApi
from image import image_grab_mss
from process import get_average_color, get_color_diff, get_whites, rgba_to_hsl
import subprocess
import os

BASE_URL = os.environ.get('HA_API_URL')
TOKEN = os.environ.get('HA_API_TOKEN')
NETWORK_CHECK_INTERVAL = 10 # seconds

def get_image_bounds(factor):
    fw = 1920
    fh = 1080

    w, h = fw*factor, fh*factor
    t, l = (fw-w) / 2, (fh-h) / 3

    return map(lambda v: round(v), [t, l, w, h])

def check_network():
    ssid = 'Telia5GHz-EE6A47'

    c = subprocess.run(
        "/Sy*/L*/Priv*/Apple8*/V*/C*/R*/airport -I | awk '/ SSID:/ {print $2}'",
        capture_output = True,
        shell=True,
        text=True
    )

    return c.stdout.strip() == ssid

@click.command()
@click.option('--log/--no-log', default=False)
@click.option('--debug/--no-debug', default=False)

def main(log, debug):
    fps = 1/60
    prevColor = [0,0,0]
    connected = False
    lastCheck = -NETWORK_CHECK_INTERVAL
    executor = WindowExecutor(max_workers=2, logging=log)
    api = HaApi(BASE_URL, TOKEN, timeout=0.5, logging=log)

    while True:
        t = time.time()

        if t - lastCheck >= NETWORK_CHECK_INTERVAL:
            connected = check_network()
            lastCheck = t

        if connected:
            img = image_grab_mss(*get_image_bounds(0.5), debug)

            avg = get_average_color(img)
            r, g, b = avg
            newColor = [r, g, b]

            if newColor != prevColor:
            #if get_color_diff(newColor, prevColor) > 8:
                prevColor = newColor

                #h, s, l = rgba_to_hsl(avg)
                #cw, ww = get_whites(avg)
                #cw, ww = (1-s)*255, s*255
                cw, ww = 125, 125

                executor.submit(api.turn_on, {
                    'entity_id': 'light.gledopto_ledstrip',
                    'rgbww_color': [*newColor, cw, ww],
                    'brightness': 255,
                    'transition': 0
                })

        duration = time.time() - t
        time.sleep(max(fps-duration, 0))

if __name__ == "__main__":
    main()