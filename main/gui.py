# -*- coding: latin-1 -*-

###   App By : Redouane            ###
###   E-MAIL : unrealdz@gmail.com  ###
###   BLOG : dzpp.blogspot.com     ### 
###   LICENSE : GNU GPL v3         ###


from __future__ import division

from PyQt4.QtGui import ( QListWidgetItem, QMainWindow, QAction, QMessageBox, QGroupBox,
QLineEdit, QPushButton, QBoxLayout, QListWidget, QProgressBar,
QLabel, QToolButton, QIcon, QPixmap, QFileDialog, QStyle )

from PyQt4.QtCore import SIGNAL, SLOT, Qt, QThread, QString
from dl import *
from os import startfile
from shutil import rmtree
import urllib

class tracklistitems(QListWidgetItem):
    def __init__(self, title):
        super(tracklistitems, self).__init__()
        self.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        self.setCheckState(Qt.Checked)
        self.setText(title)
    def eligible(self):
        if self.checkState() == 2:
            return 'Checked'
        else:
            return 'Unchecked'
       
class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setWindowTitle('DZik 1.3')
        self.icon = QIcon('images/mainwindowicon.png')
        self.setWindowIcon(self.icon)
        self.resize(520,530)
        self.setMaximumSize(520, 530)
        self.setMinimumSize(520, 530)
        self.menu = self.menuBar()
        self.Fichier = self.menu.addMenu('&Fichier')
        self.exit = QAction('Quiter', self)
        self.about = QAction('About', self)
        self.Fichier.addAction(self.about)
        self.Fichier.addAction(self.exit)
        self.connect(self.exit, SIGNAL('triggered()'), SLOT('close()'))
        self.connect(self.about, SIGNAL('triggered()'), self.launchabout)
        self.show()
    def launchabout(self):
        self.aboutbox = QMessageBox()
        self.aboutbox.about(self, 'DZik', '<b>Version</b> : 1.3 <br /> <b>Written By : </b>  Redouane <br /> <b>Blog : </b> <a href="http://dzpp.blogspot.com"> dzpp.blogspot.com </a> <br /> <b>E-mail</b> : <a href="mailto:unrealdz@gmail.com?Subject=Dz music Downloader">unrealdz@gmail.com</a> <br /> <b> Repository : </b> <a href="https://github.com/redouane/Dzik"> https://github.com/redouane/Dzik </a> <br/> <b>Supporte Actuellement : </b>  <br /> <a href="www.Douniamusic.com">www.Douniamusic.com</a> <br /> <a href="www.Zikdalgerie.com">www.Zikdalgerie.com</a>')
   
class urlgroup(QGroupBox):
    def __init__(self, parent=None):
        super(urlgroup, self).__init__(parent)
        self.setGeometry(10,30,500,80)
        self.setObjectName('urlgroup')
        self.urlbar = QLineEdit()
        self.urlbar.setObjectName('urlbar')
        self.urlbar.setText('Collez votre URL içi')
        self.urlbar.setStyleSheet('font-weight:lighter;color:gray;')
        self.urlbar.show()
        self.parsebutton = QPushButton('Go !!')
        self.parsebutton.setObjectName('parsebutton')
        self.parsebutton.show()
        layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        layout.addWidget(self.urlbar)
        layout.addWidget(self.parsebutton)
        self.show()
        self.group2 = QGroupBox(parent)
        self.group2.setObjectName('core')
        self.group2.setGeometry(10,120,500,280)
        self.group2.show()
        self.group3 = QGroupBox(self.group2)
        self.group3.setObjectName('albuminfos')
        self.group3.setGeometry(10,15,200,245)
        self.group3.show()
        self.itemlist = QListWidget(self.group2)
        self.itemlist.setGeometry(250,15,230,245)
        self.itemlist.show()
        self.dlgroup = QGroupBox(parent)
        self.dlgroup.setObjectName('dlgroup')
        self.dlgroup.setGeometry(10,420,500,100)
        self.dlgroup.show()
        self.dlgroup.dlbutton = QPushButton('Download', self.dlgroup)
        self.dlgroup.dlbutton.setObjectName('dlbutton')
        self.dlgroup.dlbutton.move(10,20)
        self.dlgroup.dlbutton.show()
        self.dlgroup.progressbar = QProgressBar(self.dlgroup)
        self.dlgroup.progressbar.setObjectName('progressbar')
        self.dlgroup.progressbar.setGeometry(100,21,380,21)
        self.dlgroup.progressbar.show()
        self.dlgroup.dlinfos = QLabel(self.dlgroup)
        self.dlgroup.dlinfos.setGeometry(100,70,200,21)
        self.dlgroup.dlinfos.show()
        self.dlgroup.dledfile = QLabel(self.dlgroup)
        self.dlgroup.dledfile.setGeometry(300,70,200,21)
        self.dlgroup.dledfile.show()
        self.dlgroup.dlto = QLineEdit('C:\\', self.dlgroup)
        self.dlgroup.dlto.setGeometry(100,50,350,21)
        self.dlgroup.dlto.show()
        self.dlgroup.dlto.changebt = QToolButton(self.dlgroup)
        self.dlgroup.dlto.changebt.setObjectName('dltobt')
        self.dlgroup.dlto.changebt.setGeometry(10,50,75,21)
        self.dlgroup.dlto.changebt.setText('To')
        self.dlgroup.dlto.changebt.show()
        self.dlgroup.dlto.openf = QPushButton('Open', self.dlgroup)
        self.dlgroup.dlto.openf.setGeometry(455,50,35,21)
        self.dlgroup.dlto.openf.setObjectName('openfolder')
        self.dlgroup.dlto.openf.show()  
        self.album = QLabel(self.group3)
        self.artist = QLabel(self.group3)
        self.year = QLabel(self.group3)
        self.tracks = QLabel(self.group3)
        self.coverart = QLabel(self.group3)
        self.urlbar.setFocus(True)
        self.connect(self.parsebutton, SIGNAL('clicked()'), self.parseclicked )
        self.connect(self.dlgroup.dlbutton, SIGNAL('clicked()'), self.launchdl)
        self.connect(self.dlgroup.dlto.changebt, SIGNAL('clicked()'), self.changedir)
        self.connect(self.dlgroup.dlto.openf, SIGNAL('clicked()'), self.openfolder)
        
    def parseclicked(self):
        self.itemlist.clear()
        url = str(self.urlbar.text())
        self.infos = getsonglist(url)
        if (self.infos == 'connexion impossible') or (self.infos == 'unsupported'):
            self.error = QMessageBox()
            if self.infos == 'connexion impossible':
                self.error.setText('Connexion Impossible !')
            elif self.infos == 'unsupported':
                self.error.setText('Site Unsupported !!')
            self.error.setWindowTitle('Erreur!')
            self.error.setIcon(QMessageBox.Warning)
            self.icon = QIcon('images/mainwindowicon.png')
            self.error.setWindowIcon(self.icon)
            self.error.exec_()
        else:
            self.artist.setText('Artiste : ' + self.infos['artist'])
            self.artist.move(40,175)
            self.artist.show()
            self.album.setText('Album : ' + self.infos['albumname'])
            self.album.move(40,190)
            self.album.show()
            try:
                self.year.setText('Annee : ' + self.infos['year'])
                
            except KeyError:
                self.year.setText('Annee : ' + 'N/A')
            self.year.move(40,205)
            self.year.show()
            self.tracks.setText('Tracks : ' + str(self.infos['tracks']))
            self.tracks.move(40,220)
            self.tracks.show()
            coverartpix = QPixmap(self.infos['coverart'])
            coverartpix = coverartpix.scaled(178,135,)
            self.coverart.setPixmap(coverartpix) 
            self.coverart.move(10,10)
            self.coverart.show()
            self.list2 = []
            for item in self.infos['titles']:
                item = tracklistitems(item)
                self.list2.append(item)
            for item in self.list2:
                self.itemlist.addItem(item)
                
            
            
            

    def launchdl(self):
        if self.dlgroup.dlbutton.text() == 'Download':
            try:
                self.itemlist.item(self.currentitem).setText(self.text)
            except:
                pass
            self.dlgroup.dlbutton.setText('Stop')
            rmtree('tmpimg', True)
            i= 0
            dllist = []
            for item in self.list2:
                if item.eligible() =='Checked':
                    dllist.append(i)
                i= i+1
            self.stritemlist = []
            for i in range(0,self.infos['tracks']):
                #print i
                #print self.itemlist.item(i).text()
                #TODO: hamida album breaks, recheck regexes
                self.stritemlist.append(str(self.itemlist.item(i).text()))
            dlto =  self.dlgroup.dlto.text()
            self.thread = dlThread(dllist, self.infos, dlto, self.stritemlist) 
            self.connect(self.thread, SIGNAL('progress(PyQt_PyObject)'), self.updateProgress)
            self.connect(self.thread, SIGNAL('dledfile(PyQt_PyObject)'), self.updateDlednow)
            self.thread.start()
        else:
            self.dlgroup.dlbutton.setText('Download')
            self.thread.terminate()
      
    def updateProgress(self, progress):
        self.dlgroup.progressbar.setValue(progress['bar'])
        self.dlgroup.dlinfos.setText(progress['info'])
        self.text = self.stritemlist[progress['item']]
        self.currentitem = progress['item']
        self.percent = str(progress['bar']) + ' % - '
        self.percent = QString(self.percent)
        self.dlingicon = QIcon('images/dling.png')
        self.doneicon = QIcon('images/done.png')
        self.itemlist.item(progress['item']).setIcon(self.dlingicon)
        self.itemlist.item(progress['item']).setText(self.percent + self.text)
        if progress['bar'] >= 98:
            self.itemlist.item(progress['item']).setIcon(self.doneicon)
            self.itemlist.item(progress['item']).setText(self.text)
            self.itemlist.item(progress['item']).setCheckState(Qt.Unchecked)
            self.itemlist.item(progress['item']).setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
            
    def updateDlednow(self, dledfile):
        self.dlgroup.dledfile.setText(dledfile)

    
    def changedir(self):
        self.dir = QFileDialog.getExistingDirectory()
        self.dlgroup.dlto.setText(self.dir + '/')
    def openfolder(self):
        startfile(self.dlgroup.dlto.text())
        
    def stopdl(self):
        pass

class dlThread(QThread): 
    def __init__(self, dllist, infos, dlto, itemlist, parent=None):
        super(dlThread, self).__init__(parent)
        self.dllist = dllist
        self.infos = infos
        self.dlto = dlto
        self.itemlist = itemlist
    def run(self):
        for item in self.dllist:
            self.item = item
            self.link = self.infos['links'][item]
            self.filename = self.dlto + self.itemlist[item] + '.mp3'
            dledfile = self.itemlist[item] + '.mp3'
            self.emit(SIGNAL('dledfile(PyQt_PyObject)'), dledfile)
            self.dltrack(self.link, self.filename)     
                 
    def dltrack(self, link, filename):
        urllib.urlretrieve(link, filename, self.reporthook)
    def progresspercent(self, sizeread, filesize):
        if sizeread <1:
            return 0
        else:
            a = filesize / sizeread
            percent = 100 / a
            return int(percent)
    def reporthook(self, blocks_read, block_size, total_size):
        filesizeko = total_size / 1024
        amount_readko = blocks_read * block_size /1024
        progress = self.progresspercent(float(amount_readko), float(filesizeko))
        dledinfo = 'Downloaded ' + str(int(amount_readko)) + 'Ko / ' + str(int(filesizeko)) + 'Ko'
        progress = {'bar':progress,'info':dledinfo, 'item':self.item}
        self.emit(SIGNAL('progress(PyQt_PyObject)'), progress)
        