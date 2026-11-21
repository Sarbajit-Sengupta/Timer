import unittest
from countdown import Countdown, parse_duration


class Scheduler:
    def __init__(self):
        self.jobs = {}
        self.sequence = 0

    def after(self, delay, callback):
        self.sequence += 1
        self.jobs[self.sequence] = callback
        return self.sequence

    def after_cancel(self, key):
        del self.jobs[key]


class CountdownTests(unittest.TestCase):
    def test_hour_restart_and_elapsed_time(self):
        now, frames, finished = [10], [], []
        scheduler = Scheduler()
        timer = Countdown(scheduler, lambda *v: frames.append(v),
                          lambda: finished.append(True), clock=lambda: now[0])
        timer.start(3600)
        self.assertEqual(frames[-1], (1, 0, 0))
        timer.start(2)
        self.assertEqual(len(scheduler.jobs), 1)
        now[0] += 5  # late event-loop callback must use elapsed time
        callback = scheduler.jobs.pop(timer.pending)
        callback()
        self.assertEqual(frames[-1], (0, 0, 0))
        self.assertEqual(finished, [True])
        self.assertFalse(scheduler.jobs)

    def test_invalid_duration(self):
        for values in [('x', '0', '0'), ('-1', '0', '0'), ('', '0', '0')]:
            with self.assertRaises(ValueError):
                parse_duration(*values)
        self.assertEqual(parse_duration('1', '0', '0'), 3600)


if __name__ == '__main__':
    unittest.main()
