import PyInstaller.__main__

PyInstaller.__main__.run([
    'app.py',
    '-F',
    '-w',
    '-i=app.ico'
])