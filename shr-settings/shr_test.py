import elementary, module

class Test(module.AbstractModule):
    def totest(self, obj, event, *argns, **kargs):
        print event
        print "it works!"
        obj.label_set("lol")
    def name(self, ):
        print "name"
        return "Test"
    def enabled(self, ):
        return 0
    def view(self, win):
        bt = elementary.Button(win)
        bt.clicked = self.totest
        bt.label_set("Just for fun")
        bt.size_hint_align_set(-1.0, 0.0)
        bt.show()

        return bt


if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
