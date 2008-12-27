import module, elementary

class Clock(module.AbstractModule):
    def name(self):
        return "Date/time"
    def view(self, win):
        cl = elementary.Clock(win)
        return cl

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
