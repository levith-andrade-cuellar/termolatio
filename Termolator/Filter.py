import nltk
import re, pickle, logging, os
from nltk.corpus import stopwords # not encumbered by license, see stopwords.readme()
nltk.download('stopwords')

## abbreviations={}
stops = []
dir_name = os.path.dirname(os.path.realpath(__file__)) + os.sep
logger = logging.getLogger()

def _get_stops(filename=dir_name + 'patentstops.txt'):
    """Import stop words either from a text file or stopwords corpus"""
    global stops
    try:
        with open(filename, 'r') as f:
            stops = [line.strip() for line in f]
    except FileNotFoundError:
        stops = stopwords.words('spanish')

def _reGlue(words):
    """Helper function to turn a list of words into a string"""
    ret = ""
    for i in range(len(words)):
        ret += words[i] + " "
    ret = ret.strip()
    return ret

def removeStops(string): #NOT NEEDED AS NP EXTRACTING REMOVES THEM
    """Strip stop words off the beginning and ending of a phrase"""
    global stops
    if not stops:
        _get_stops()
    # entire phrase in stops
    if string in stops:
        return ""
    words = string.split()
    if not words:
        return ""
    # beginning stops (loses case of multiword stops)
    while words[0] in stops:
        words.pop(0)
        if not words:
            return ""
    # ending stops (loses case of multiword stops)
    while words[-1] in stops:
        words.pop(0)
        if not words:
            return ""
    string = _reGlue(words)
    return string

def bad_unicode(string):
    for char in string:
        if ord(char)>127:
            ## print(char)
            return(True) 
            
def remove_non_unicode(string):
    output = ''
    for char in string:
        if ord(char)>127:
            output=output+' '
        else:
            output=output+char
    output = output.strip(' ')
    return(output)

def lowercase(string):
    """Return an all lowercase representation of a string"""
    return string.lower()
def isWord(string):
    """Test the legitimacy of the proposed phrase. Taken from Shasha's implementation"""
    #criteria:
    pattern = re.compile(r"""
(
&lt
|%
|/
|\\
|&\ lt
|\)
|\(
|\.
|\+
|and\
|\ and
|\ and\
)
""", re.I | re.VERBOSE | re.UNICODE)
    if len(string) < 2:
        return ''
    elif re.findall(pattern, string):
        return ''
    #must contain at least one letter
    for i in range(len(string)):
        if string[i].isalpha():
            return string
    return ''

# available filters:    
criteria={### 'abbreviation': expand, ## abbreviation expansion is handled by earlier processes now
          'stops': removeStops,
          'case': lowercase,
          'isWord': isWord}
