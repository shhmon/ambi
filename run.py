import time
import click
from executor import WindowExecutor
from api import HaApi
from image import image_grab_mss
from process import get_average_color, get_color_diff, get_whites, rgba_to_hsl
import os



BASE_URL = os.environ.get('HA_API_URL')
TOKEN = os.environ.get('HA_API_TOKEN')

def get_image_bounds(factor):
    fw = 1920
    fh = 1080

    w, h = fw*factor, fh*factor
    t, l = (fw-w) / 2, (fh-h) / 3

    return map(lambda v: round(v), [t, l, w, h])

@click.command()
@click.option('--log/--no-log', default=False)
@click.option('--debug/--no-debug', default=False)
def main(log, debug):
    fps = 1/60
    prevColor = [0,0,0]
    executor = WindowExecutor(max_workers=2, logging=log)
    api = HaApi(BASE_URL, TOKEN, timeout=0.5, logging=log)

    while True:
        t = time.time()

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