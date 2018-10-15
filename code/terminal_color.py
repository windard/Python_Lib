# coding=utf-8

class bcolors:
    BLUE = '\033[95m'
    WHITE = '\033[94m'
    BLACK = '\033[92m'
    GRAY = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


print bcolors.BLUE + "First color is blue " + bcolors.ENDC
print bcolors.WHITE + "Second is white" + bcolors.ENDC
print bcolors.BLACK + "Second is black" + bcolors.ENDC
print bcolors.GRAY + "Second is gray" + bcolors.ENDC
print bcolors.RED + "Second is red" + bcolors.ENDC