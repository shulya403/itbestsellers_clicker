import os
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=%s' % "selen",
    '--onefile',

    #'--windowed',

    'selen_bestsellers.py'
])