# coding=utf-8

import platform

print platform.system()
print platform.version()
print platform.release()
print platform.dist()
print platform.uname()
print platform.node()
print platform.platform()
print platform.machine()
print platform.processor()
print platform.architecture()
print platform._sys_version()
print platform.java_ver()
print platform.python_version()
print platform.python_implementation()
print platform.python_version_tuple()
print platform.python_branch()
print platform.python_compiler()
print platform.python_build()
print platform.win32_ver()
print platform.mac_ver()
print platform.linux_distribution()

print platform.popen('ifconfig','w')
