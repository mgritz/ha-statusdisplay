import threading
import os
import sys

from time import sleep
from queue import Queue

from PIL import Image,ImageDraw,ImageFont

waveshare_libdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'e-Paper', 'RaspberryPi_JetsonNano', 'python', 'lib')
if os.path.exists(waveshare_libdir):
    sys.path.append(waveshare_libdir)
from waveshare_epd import epd2in15g

class DisplayItem:
    def __init__(self, title, value, visible=False):
        self.title = title
        self.value = value
        self.visible = visible

    def __str__(self):
        return f"{self.title}: {self.value}"

    def __eq__(self, value: object) -> bool:
        return (isinstance(value, DisplayItem)
                and self.title == value.title
                and self.value == value.value
                and self.visible == value.visible)

class DisplayUpdater(threading.Thread):
    def __init__(self):
        super().__init__()
        self.items = {}
        self.q = Queue()

        self.font12 = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                'Roboto', 'Roboto-VariableFont_wdth,wght.ttf'), 12)

        try:
            self.epd = epd2in15g.EPD()
            self.epd.init()
            self.epd.Clear()
        except IOError as e:
            print("Failed to initialize e-Paper display:", e)
            self.epd = None

    def run(self):

        while True:
            item = self.q.get() # Blocking infinitely if no news
            if item is None:
                break  # Exit signal

            update_needed = False
            sleep(1) # Batch updates

            while item is not None:
                if (item.title not in self.items or
                        self.items[item.title] != item):
                    update_needed = True
                    self.items[item.title] = item
                if not self.q.empty():
                    item = self.q.get()
                else:
                    item = None

            if update_needed:
                self.update_display()


    def update_display(self):
        Himage = Image.new('RGB', (self.epd.height, self.epd.width), self.epd.WHITE)
        draw = ImageDraw.Draw(Himage)

        for item in self.items.values():
            if item.visible:
                print(f"- {item}")
                draw.text((0, 12 * list(self.items.keys()).index(item.title)),
                          f"{item.title}: {'OFFEN' if item.value else 'zu'}",
                          font=self.font12, fill=self.epd.BLACK)

        try:
            self.epd.display(self.epd.getbuffer(Himage))
        except IOError as e:
            print("Failed to update e-Paper display:", e)

    def stop(self):
        self.q.put(None)  # Send exit signal to the thread

    def notify(self, title, value, visible=True):
        self.q.put(DisplayItem(title, value, visible))

