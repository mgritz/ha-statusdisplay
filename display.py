import threading
from time import sleep
from queue import Queue

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
        print("Current MQTT Topics and Messages:")
        for item in self.items.values():
            if item.visible:
                print(f"- {item}")

    def stop(self):
        self.q.put(None)  # Send exit signal to the thread

    def notify(self, title, value, visible=True):
        self.q.put(DisplayItem(title, value, visible))

