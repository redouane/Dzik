# -*- coding: latin_1 -*-
from distutils.core import setup
import py2exe

# --packages encodings.latin_1

setup(name = 'Dzik Downloader',
			version = '1.3',
			author ='Redouane',
			author_email="unrealdz@gmail.com", 
			data_files = [('images', ['images/mainwindowicon.png', 'images/headset-icon.png', 'images/musicnote.png', 'images/dling.png', 'images/done.png']), ('.', ['style.qss'])],
			windows=[ { 
							"script": 'dzik.py',
							"icon_resources": [(1, "images/app.ico") ]

					} ],
	
			options={"py2exe": {"includes": ["sip"]}}) 
			
			
