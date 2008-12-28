import module, elementary

class Clock(module.AbstractModule):
    def name(self):
        return "Date/time"
    def view(self, win):
        cl = elementary.Clock(win)
        cl.show_seconds_set(True)
        return cl
