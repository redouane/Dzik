# -*- coding: latin-1 -*-

###   App By : Redouane            ###
###   E-MAIL : unrealdz@gmail.com  ###
###   BLOG : dzpp.blogspot.com     ### 
###   LICENSE : GNU GPL v3         ###




from main import gui
from PyQt4.QtGui import QApplication, QMessageBox
from PyQt4.QtCore import QThread, SIGNAL
import urllib
import re
import sys


if hasattr(sys,"setdefaultencoding"):
    sys.setdefaultencoding("latin-1")
    
currentversion = '1.3'
def main(): 
    class App(QApplication):
        def __init__(self, argv):
            super(App, self).__init__(argv)
            css = open('style.qss', 'r').read()
            self.main = gui.Mainwindow()
            self.urlbar = gui.urlgroup(self.main)
            self.setStyleSheet(css)
            self.thread = checkforUpdate()
            self.connect(self.thread, SIGNAL('updateinfos(PyQt_PyObject)'), self.update)
            self.thread.start()
        def update(self, updateinfos):
            self.updatebox = QMessageBox()
            self.updatebox.about(self.main, 'Mise à  jour', 'Une nouvelle Mise à  jour est disponible  : <br \> <b> Version : </b>' + updateinfos['version'] + '<br /> <b> Lien : </b>' + updateinfos['link'] + '<br /> <b>Nouveautés : </b>' + updateinfos['whatsnew'])
              
    class checkforUpdate(QThread):
        def run(self):
            xml = 'http://dl.dropbox.com/u/6858914/DZik/DZik.xml'
            try:
                xml = urllib.urlopen(xml).read()
                latestversion = re.findall('<version>(.+)</version>', xml)[0]
                if float(latestversion) <= float(currentversion):
                    return
                else:
                    link = re.findall('<link>(.+)</link>', xml)[0]
                    whatsnew = re.findall('<whatsnew>(.+)</whatsnew>', xml)[0]
                    updateinfos = {'version':latestversion, 'link':link , 'whatsnew':whatsnew}
                    self.emit(SIGNAL('updateinfos(PyQt_PyObject)'), updateinfos)
            except IOError:
                return
    
    dzik = App(sys.argv)
    dzik.exec_()
    
if __name__ == '__main__':
    main()