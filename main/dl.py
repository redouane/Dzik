# -*- coding: latin-1 -*-

###   App By : Redouane            ###
###   E-MAIL : unrealdz@gmail.com  ###
###   BLOG : dzpp.blogspot.com     ### 
###   LICENSE : GNU GPL v3         ###


import re
import urllib
import urllib2
import urlparse
from os import mkdir, path

def changeuserAgent():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener

def stripalbumname(url):
    """ takes an url as str returns album name"""
    return re.findall('Album-(.+).php', url)[0]

def dlcover(coverart, saveas):
    """ takes cover link, dls it returns local file string"""
    if not path.exists('tmpimg'):
        mkdir('tmpimg')
    try:
        urllib.urlretrieve(coverart, 'tmpimg/' + saveas)
    except IOError:
        return 'connexion impossible'
    return 'tmpimg/' + saveas
    
    

def getsonglist(url):
    res = urlparse.urlparse(url)
    if res[0] !='http':
        url = urlparse.urljoin('http:////', url)
        hostname = urlparse.urlparse(url).hostname
    else:
        hostname = urlparse.urlparse(url).hostname
    opener = changeuserAgent()
    if hostname == 'www.douniamusic.com':
        try:
            
            xml = urllib.urlopen('http://dl.dropbox.com/u/6858914/DZik/DZik.xml').read()
            html = opener.open(url).read()
            idquery = re.findall('<albumid>(.+)</albumid>', xml)[0]
            xmlquery = re.findall('<xmlquery>(.+)</xmlquery>', xml)[0]
        except IOError:
            return 'connexion impossible'
        albumID = re.findall(idquery, html)[0]
        xml = opener.open(xmlquery + albumID).read()
        artist = urllib.unquote(re.findall('<artist>(.+)</artist>', xml)[0])
        titles = re.findall('<title>(.+)</title>', xml)
        titlesd = []
        for item in titles: 
            titlesd.append(urllib.unquote(item))
        albumname = urllib.unquote(re.findall('<album>(.+)</album>', xml)[0])
        filetype = re.findall('<filetype>(.+)</filetype>', xml)[0]
        year = re.findall('<year>(.+)</year>', xml)[0]
        tracks = len(titles)
        coverart = 'http://www.douniamusic.com/album-miniature/' + albumID +'.jpg'
        saveas = str(albumID) + '.png'
        coverart = dlcover(coverart, saveas)
        
        links = re.findall('<filename>(.+)</filename>', xml)
        linksd = []
        for item in links:
            linksd.append(urllib.unquote(item))
        return {'albumID':albumID, 'artist':artist,'albumname':albumname, 'titles':titlesd, 'year':year, 'tracks':tracks, 'coverart':coverart, 'links':linksd}
    elif hostname == 'dzmusique':
         return 'unsupported'
    elif hostname =='www.zikdalgerie.com':
        try:
            html = opener.open(url).read()
        except IOError:
            return 'connexion impossible'
        htmlurl = re.findall("wimpyApp=(.+)&&background_color", urllib.unquote(html))[0]
        albumID = re.findall("pid=(.+)host", html)[0]
        xml = opener.open(htmlurl + '&?action=getstartupdirlist').read()
        links = re.findall("&item\d+=(http:[()\s./a-zA-Z0-9_-]+)", urllib.unquote(xml))
        titles = re.findall("\|([^\|]+)\|{2}", urllib.unquote(xml))
        coverart = re.findall("visualURL=(http:[()\s./a-zA-Z0-9_-]+)", urllib.unquote(xml))[0]
        tracks = int(re.findall("&totalitems=(\d+)", urllib.unquote(xml))[0])
        saveas = albumID + '.jpg'
        coverart = dlcover(coverart, saveas)
        info = re.findall("""<h4 style="font-size:12pt;color:#000000">(.+)</h4>""", html)[0].split('-')
        artist = info[0]
        albumname = info[1]
        
        return {'albumID':albumID, 'artist':artist,'albumname':albumname, 'titles':titles, 'tracks':tracks, 'coverart':coverart, 'links':links}
    
    else:
        return 'unsupported'
    
   
