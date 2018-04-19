# -*- coding: utf-8 -*-

import subprocess

if __name__ == '__main__':
    retcode = subprocess.call(["which", "pbcopy"])
    print subprocess.check_call(["which", "pbcopy"])
    print subprocess.check_output(["which", "pbcopy"])
    print retcode

    p = subprocess.Popen(["which", "pbcopy"], stdout=subprocess.PIPE)
    print p.wait()

    out, err = p.communicate()
    print out
