"""One monotonic, nonblocking countdown driven by a Tk-compatible scheduler."""
import math
import time


def parse_duration(hours, minutes, seconds):
    values = tuple(int(value) for value in (hours, minutes, seconds))
    if any(value < 0 for value in values):
        raise ValueError("Time values must be nonnegative")
    return values[0] * 3600 + values[1] * 60 + values[2]


class Countdown:
    def __init__(self, scheduler, display, finished, clock=time.monotonic):
        self.scheduler = scheduler
        self.display = display
        self.finished = finished
        self.clock = clock
        self.pending = None
        self.deadline = 0

    def cancel(self):
        if self.pending is not None:
            self.scheduler.after_cancel(self.pending)
            self.pending = None

    def start(self, seconds):
        self.cancel()
        self.deadline = self.clock() + seconds
        self.tick()

    def tick(self):
        self.pending = None
        remaining = max(0, math.ceil(self.deadline - self.clock()))
        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.display(hours, minutes, seconds)
        if remaining == 0:
            self.finished()
        else:
            self.pending = self.scheduler.after(100, self.tick)
