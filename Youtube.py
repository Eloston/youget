'''
    This file is part of youget.

    youget is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    youget is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with youget. If not, see <http://www.gnu.org/licenses/>.
'''
import io
import urllib.request
import urllib.parse
import re
import binascii
import http.client
import os.path
import sys
import html.parser

parser = html.parser.HTMLParser()

def downloadpage(URL):
    '''
    Downloads the page at the URL
    '''
    try:
        youtubeobj = urllib.request.urlopen(URL)
    except:
        return 'Error_OpeningURL'
    try:
        rawdata = youtubeobj.read()
    except:
        return 'Error_ReadingData'
    try:
        youtubedata = rawdata.decode("UTF-8")
    except:
        youtubeobj.close()
        del youtubeobj
        return 'Error_DecodingData'
    youtubeobj.close()
    del youtubeobj
    youtubedata = youtubedata.replace('\n', '')
    return youtubedata

def decodeHTMLescape(DATA):
    global parser
    return parser.unescape(DATA)

def getmeta(youtubedata):
    '''
    Takes data from downloadpage()
    Retrieves title, description, author, upload date, views, likes, and dislikes from data.
    '''
    titlematch = re.search(r'<meta name="title" content="(?P<Title>.*?)">', youtubedata)
    descriptionmatch = re.search(r'<p id="eow-description"( )?>(?P<Description>.*?)</p>', youtubedata)
    authormatch = re.search(r'class="yt-user-name author" rel="author" dir="ltr"( )?>(?P<Author>.*?)</a>', youtubedata)
    datematch = re.search(r'<span id="eow-date" class="watch-video-date"( )?>(?P<Date>.*?)</span>', youtubedata)
    viewsmatch = re.search(r'<span class="watch-view-count">( )*?<strong>(?P<Views>.*?)</strong>', youtubedata)
    likesmatch = re.search(r'<span class="likes"( )?>(?P<Likes>.*?)</span>', youtubedata)
    dislikesmatch = re.search(r'<span class="dislikes"( )?>(?P<Dislikes>.*?)</span>', youtubedata)

    if titlematch == None:
        title = "N/A"
    else:
        title = decodeHTMLescape(titlematch.group("Title"))

    if descriptionmatch == None:
        description = "N/A"
    else:
        description = decodeHTMLescape(descriptionmatch.group("Description"))

    if authormatch == None:
        author = "N/A"
    else:
        author = decodeHTMLescape(authormatch.group("Author"))

    if datematch == None:
        date = "N/A"
    else:
        date = decodeHTMLescape(datematch.group("Date"))

    if viewsmatch == None:
        views = "N/A"
    else:
        views = decodeHTMLescape(viewsmatch.group("Views"))

    if likesmatch == None:
        likes = "N/A"
    else:
        likes = decodeHTMLescape(likesmatch.group("Likes"))

    if dislikesmatch == None:
        dislikes = "N/A"
    else:
        dislikes = decodeHTMLescape(dislikesmatch.group("Dislikes"))

    return [title, description, author, date, views, likes, dislikes]

def getflashvars(youtubedata):
    '''
    Takes data from downloadpage()
    Returns the contents of the flashvars variable
    '''
    flashvarsmatch = re.match(r'.*?flashvars=\\"(?P<VideoData>.*)\\" *allowscriptaccess', youtubedata)
    if flashvarsmatch == None:
        Stuff = ''
    else:
        Stuff = flashvarsmatch.group("VideoData")
    for iteration in range(0, 20):
        Stuff = urllib.parse.unquote(Stuff)
        if not ("%" in Stuff):
            break
    Stuff = bytes(Stuff, 'UTF-8').decode('unicode-escape')
    return Stuff

def getvideourl(DATA):
    '''
    Takes in the data from getyoutubeblob()
    Returns URLS as well as meta-information about the video if it's avaliable.
    '''
    urldata = dict()
    for match in re.finditer(r'[,=]url=(?P<VideoURL>http://.+?&id=.+?)((&quality=(?P<Quality>.+?)&)|&)(.*?&type=video/(?P<VideoType>.+?)(&|(;\+codecs="(?P<VideoCodecs>.*?)"&))(url=)?)?', DATA):
        datalist = [match.group("VideoURL"), match.group("VideoType"), match.group("VideoCodecs"), match.group("Quality")]
        for item in datalist:
            if item == None:
                datalist[datalist.index(item)] = "N/A"
        urldata[datalist[0]] = [datalist[1], datalist[2], datalist[3]]
    return urldata

def getvideosize(URL):
    '''
    Returns the size of the video URL via HTTP header
    '''
    try:
        host = urllib.parse.urlparse(URL)
        connectionobject = http.client.HTTPConnection(host.netloc)
        connectionobject.request("HEAD", URL)
        responseobject = connectionobject.getresponse()
        length = responseobject.getheader('Content-Length')
        connectionobject.close()
    except:
        try:
            connectionobject.close()
        except:
            pass
        length = None
    return length

def programfile_path(FILENAME):
    '''
    Return absolute path to a file in the program's directory
    '''
    basepath = os.path.dirname(__file__)
    final_path = os.path.join(basepath, FILENAME)
    return final_path

def loadlaunchcommand(PATH):
    if os.path.isfile(PATH):
        with open(PATH) as FILE:
            commanddict = dict()
            for line in FILE:
                linematch = re.match(r'{(?P<Name>.+?)\|\|(?P<Command>.+)}', line)
                if linematch == None:
                    commanddict["Nothing loaded"] = ''
                    return commanddict
                Name = linematch.group("Name")
                Command = linematch.group("Command")
                if Name == None:
                    Name = "(Unnamed command)"
                if Command == None:
                    Name = Name + "(command broken)"
                    Command = ''
                commanddict[Name] = Command
            return commanddict
    else:
        return None

def launchcommand(command):
    os.system(command)
