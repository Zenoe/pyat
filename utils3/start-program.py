#!/usr/bin/env python3

import subprocess

paramList = [
    'C:\\Apps\\cygwin\\bin\\mintty.exe',
    '-'
]
# subprocess.call(['C:\\Temp\\a b c\\Notepad.exe', 'C:\\test.txt'])
subprocess.call(paramList)

# program = subprocess.Popen(['c:/cygwin/bin/mintty.exe', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# program.stdin.write("command1")
# stdout1, stderr1 = program.communicate()

# program.stdin.write(change_something(stdout1))
# stdout2, stderr2 = program.communicate()
