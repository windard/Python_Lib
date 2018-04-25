# coding=utf-8

from halo import Halo

spinner = Halo(text='Loading', spinner='dots')
spinner.start()

# Run time consuming work here
# You can also change properties for spinner as and when you want

spinner.stop()
