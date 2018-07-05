from config import Load
import os
HOME = os.environ['HOME']
def touchplaces():
        places = Load("/var/tmp/places")
        userdirs = []
        with open ("{}{}".format(HOME, "/.config/user-dirs.dirs")) as dirs:
                lines = dirs.read()
        for test in lines.splitlines():
                if test.startswith ("#") is not True:
                        start = test.find("$") + 1
                        end = test.find('"')
                        dir = test[start:end-start + 1].replace("HOME", 
                        "~")
                        places.set("{}".format(dir), 
                                "{},{},{}".format(os.path.basename(dir), 
                                "Folder", 
                                True))
                        
