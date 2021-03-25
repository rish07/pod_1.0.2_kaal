from AppKit import NSWorkspace
import time

to_send = {}


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        #print("Elapsed time:", elapsed_time * 100, "seconds")
        return elapsed_time * 100


while True:
    activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    active = activeAppName
    t = Timer()
    t.start()
    activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    if (active != activeAppName):
        elapsed = t.stop()
        to_send[activeAppName] = elapsed
        print(to_send)
