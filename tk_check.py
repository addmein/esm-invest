from Tkinter import *
import tkMessageBox
from ESM_dictionaries import dict


dictlist = []
for key, value in dict['languages'].iteritems():
    dictlist.append(value)

#print dict['languages']
#print dictlist

class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
            
    def state(self):
        return map((lambda var: var.get()), self.vars)


root = Tk()
lng = Checkbar(root, dictlist)
lng.pack(side=TOP, fill=X)
lng.config(relief=GROOVE, bd=2)

def allstates():
#    print "lngstate %s" %list(lng.state())
    lng_proc = []
    for value in [value for value, x in enumerate(lng.state()) if x == 1]:
#        print value, dictlist[value]
        lng_proc.append(dictlist[value])
    return lng_proc
    
def verify():
    if tkMessageBox.askyesno("ESM Investigator", "Ready to process the following languages?\n %s" %list_lang()):
        root.destroy()
#        print "Processing languages. Please wait..."
        print allstates()

def list_lang():
    return '\n' + '\n'.join(str(p) for p in allstates())
    

Button(root, text="Proceed", command=verify).pack(side=RIGHT)
Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
    
root.mainloop()