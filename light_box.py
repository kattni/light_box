"""Code for table top light box photo studio."""
import time
import board
import adafruit_dotstar
import terminalio
from adafruit_featherwing import minitft_featherwing
from adafruit_display_text import label
import displayio
from grid_layout import GridLayout

# Set watch dog timer duration in minutes. Turns off LEDs once duration is completed.
WDT_DURATION = 8

mini_tft_fw = minitft_featherwing.MiniTFTFeatherWing()

NUM_PIXELS = ((9 * 4) + (17 * 4)) * 3  # Each of 3 panels is 9 cool LEDs x 4 and 17 warm LEDs x 4
pixels = adafruit_dotstar.DotStar(board.D11, board.D12, NUM_PIXELS, brightness=1, auto_write=False)

COLOR_BALANCE = 0.5

FONT = terminalio.FONT
COLOR = 0xFF00FF

panel_label = label.Label(font=FONT, text="#", max_glyphs=50, color=COLOR)
panel_one = label.Label(font=FONT, text="1", max_glyphs=50, color=COLOR)
panel_two = label.Label(font=FONT, text="2", max_glyphs=50, color=COLOR)
panel_three = label.Label(font=FONT, text="3", max_glyphs=50, color=COLOR)

brightness_label = label.Label(font=FONT, text="Bright", max_glyphs=50, color=COLOR)
brightness_info_one = label.Label(font=FONT, max_glyphs=50, color=COLOR)
brightness_info_one.text = "{}".format(int(pixels.brightness * 100))
brightness_info_two = label.Label(font=FONT, max_glyphs=50, color=COLOR)
brightness_info_two.text = "{}".format(int(pixels.brightness * 100))
brightness_info_three = label.Label(font=FONT, max_glyphs=50, color=COLOR)
brightness_info_three.text = "{}".format(int(pixels.brightness * 100))

active_label = label.Label(font=FONT, text="Active", max_glyphs=50, color=COLOR)
active_one = label.Label(font=FONT, text="", max_glyphs=50, color=COLOR)
active_two = label.Label(font=FONT, text="", max_glyphs=50, color=COLOR)
active_three = label.Label(font=FONT, text="", max_glyphs=50, color=COLOR)

select_label = label.Label(font=FONT, text="Sel", max_glyphs=50, color=COLOR)
select_one = label.Label(font=FONT, text="", max_glyphs=50, color=COLOR)
select_two = label.Label(font=FONT, text="", max_glyphs=50, color=COLOR)
select_three = label.Label(font=FONT, text="", max_glyphs=50, color=COLOR)
select_temp = label.Label(font=FONT, text="", max_glyphs=50, color=COLOR)

temp_info = label.Label(font=FONT, text="Temp: WARM <{:3}> COOL".format(int(COLOR_BALANCE * 100)),
                        max_glyphs=50, color=COLOR)

display_group = displayio.Group(max_size=3)

layout = GridLayout(
    x=0, y=0,
    width=160, height=80,
    grid_size=(6, 5), child_padding=5,
    max_children=(7 * 4)
)

layout.add_sub_view(panel_label, grid_position=(0, 0), view_grid_size=(1, 1))
layout.add_sub_view(panel_one, grid_position=(0, 1), view_grid_size=(1, 1))
layout.add_sub_view(panel_two, grid_position=(0, 2), view_grid_size=(1, 1))
layout.add_sub_view(panel_three, grid_position=(0, 3), view_grid_size=(1, 1))
layout.add_sub_view(brightness_label, grid_position=(1, 0), view_grid_size=(1, 1))
layout.add_sub_view(brightness_info_one, grid_position=(1, 1), view_grid_size=(1, 1))
layout.add_sub_view(brightness_info_two, grid_position=(1, 2), view_grid_size=(1, 1))
layout.add_sub_view(brightness_info_three, grid_position=(1, 3), view_grid_size=(1, 1))
layout.add_sub_view(active_label, grid_position=(3, 0), view_grid_size=(1, 1))
layout.add_sub_view(active_one, grid_position=(3, 1), view_grid_size=(1, 1))
layout.add_sub_view(active_two, grid_position=(3, 2), view_grid_size=(1, 1))
layout.add_sub_view(active_three, grid_position=(3, 3), view_grid_size=(1, 1))
layout.add_sub_view(select_label, grid_position=(5, 0), view_grid_size=(1, 1))
layout.add_sub_view(select_one, grid_position=(5, 1), view_grid_size=(1, 1))
layout.add_sub_view(select_two, grid_position=(5, 2), view_grid_size=(1, 1))
layout.add_sub_view(select_three, grid_position=(5, 3), view_grid_size=(1, 1))
layout.add_sub_view(select_temp, grid_position=(5, 4), view_grid_size=(1, 1))
layout.add_sub_view(temp_info, grid_position=(0, 4), view_grid_size=(1, 1))

display_group.append(layout)
mini_tft_fw.display.show(display_group)

panels = [
    {
        "brightness": 0.2,
        "brightness_value": brightness_info_one,
        "active": True,
        "active_state": active_one,
        "selected": True,
        "selected_state": select_one,
        "warm": [0, 68],
        "cool": [68, 104],
    },
    {
        "brightness": 0.2,
        "brightness_value": brightness_info_two,
        "active": True,
        "active_state": active_two,
        "selected": True,
        "selected_state": select_two,
        "warm": [104, 172],
        "cool": [172, 208],
    },
    {
        "brightness": 0.2,
        "brightness_value": brightness_info_three,
        "active": True,
        "active_state": active_three,
        "selected": True,
        "selected_state": select_three,
        "warm": [208, 276],
        "cool": [276, 312],
    }
]

SELECTED = 0
PIXELS_ON = True
timer_start = time.monotonic()
while True:
    button = mini_tft_fw.buttons

    time.sleep(0.1)

    for panel_number, panel in enumerate(panels):
        panel["active_state"].text = "*" if panel["active"] else ""
        panel["selected_state"].text = "<" if SELECTED == panel_number else ""
        panel["brightness_value"].text = "{}".format(int(panel["brightness"] * 100))
        cool_brightness = int(255 * panel["brightness"] * (1.0 - COLOR_BALANCE)) \
            if panel["active"] and PIXELS_ON else 0
        warm_brightness = int(255 * panel["brightness"] * COLOR_BALANCE * (1.0 * (36 / 68))) \
            if panel["active"] and PIXELS_ON else 0
        warm_leds = (warm_brightness, warm_brightness, warm_brightness)
        cool_leds = (cool_brightness, cool_brightness, cool_brightness)
        pixels[panel["warm"][0]:panel["warm"][1]] = [warm_leds] * (panel["warm"][1] -
                                                                   panel["warm"][0])
        pixels[panel["cool"][0]:panel["cool"][1]] = [cool_leds] * (panel["cool"][1] -
                                                                   panel["cool"][0])
        pixels.show()

    if button.up:
        SELECTED = (SELECTED - 1) % 4
        timer_start = time.monotonic()

    if button.down and SELECTED >= 0:
        SELECTED = (SELECTED + 1) % 4
        timer_start = time.monotonic()

    select_temp.text = "<" if SELECTED == 3 else ""
    if SELECTED == 3:
        if button.right:
            COLOR_BALANCE = min(1.0, COLOR_BALANCE + 0.025)
        if button.left:
            COLOR_BALANCE = max(0, COLOR_BALANCE - 0.025)
        temp_info.text = "Temp: WARM <{:3}> COOL".format(int(COLOR_BALANCE * 100))
        continue

    if button.right:
        for panel in panels:
            if panel["active"]:
                panel["brightness"] = min(1.0, panel["brightness"] + 0.025)
        timer_start = time.monotonic()

    if button.left:
        for panel in panels:
            if panel["active"]:
                panel["brightness"] = max(0, panel["brightness"] - 0.025)
        timer_start = time.monotonic()

    if button.a:
        BRIGHTNESS = False
        for panel in panels:
            if panel["active"] and BRIGHTNESS is False:
                BRIGHTNESS = panel["brightness"]
            panel["active"] = True
        for panel in panels:
            panel["brightness"] = BRIGHTNESS if BRIGHTNESS else 0.2
        timer_start = time.monotonic()

    if button.b:
        panels[SELECTED]["active"] = not panels[SELECTED]["active"]
        time.sleep(0.15)
        timer_start = time.monotonic()

    if button.select:
        PIXELS_ON = not PIXELS_ON
        time.sleep(0.15)
        timer_start = time.monotonic()

    if time.monotonic() > (timer_start + (60 * WDT_DURATION)):
        PIXELS_ON = False
