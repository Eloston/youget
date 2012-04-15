import io
import urllib.request
import urllib.parse
import re
import binascii
import http.client
import os.path
import sys

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

def getmeta(youtubedata):
    '''
    Takes data from downloadpage()
    Retrieves title and description from data.
    '''
    titlematch = re.search(r'<meta name="title" content="(?P<Title>.*?)">', youtubedata)
    descriptionmatch = re.search(r'<p id="eow-description"( )?>(?P<Description>.*?)</p>', youtubedata)
    return [titlematch.group("Title"), descriptionmatch.group("Description")]

def getflashvars(youtubedata):
    '''
    Takes data from downloadpage()
    Returns the contents of the flashvars variable
    '''
    flashvarsmatch = re.search(r'.*?flashvars=\\"(?P<VideoData>.*)\\" *allowscriptaccess', youtubedata)
    if not flashvarsmatch == None:
        Stuff = flashvarsmatch.group("VideoData")
    while "%" in Stuff:
        Stuff = urllib.parse.unquote(Stuff)
    Stuff = bytes(Stuff, 'UTF-8').decode('unicode-escape')
    return Stuff

def getvideourl(DATA):
    '''
    Takes in the data from getyoutubeblob()
    Returns URLS as well as meta-information about the video if it's avaliable.
    '''
    urlre = re.compile(r'[,=]url=(?P<VideoURL>http://.+?&id=.+?)&(.*?&type=video/(?P<VideoType>.+?)(&|(;\+codecs="(?P<VideoCodecs>.*?)"&))(url=)?)?')
    urldata = dict()
    for match in urlre.finditer(DATA):
        urldata[match.group("VideoURL")] = [match.group("VideoType"), match.group("VideoCodecs")]
    return urldata

def getvideosize(URL):
    '''
    Returns the size of the video URL via HTTP header
    '''
    host = urllib.parse.urlparse(URL)
    connectionobject = http.client.HTTPConnection(host.netloc)
    connectionobject.request("HEAD", URL)
    responseobject = connectionobject.getresponse()
    length = responseobject.getheader('Content-Length')
    connectionobject.close()
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
                linematch = re.search(r'{(?P<Name>.+?)\|\|(?P<Command>.+)}', line)
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
