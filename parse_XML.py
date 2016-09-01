# tasks to be done:
#     The program will prompt for a URL,
# read the XML data from that URL using
# urllib and then parse and extract the
# comment counts from the XML data,
# compute the sum of the numbers in the file.

import urllib
import xml.etree.ElementTree as EleTree

# prompt for url
url = raw_input('Enter url: ').strip()

# get xml
try:
    xml = urllib.urlopen(url).read()
    # print xml
except:
    print 'bad input, program finishes'
    quit

# get tree
tree = EleTree.fromstring(xml)
    
# sum numbers
sum = 0

# print tree.findall('comment')

for comment in tree.findall('comments/comment'): 
    num = int(comment.find('count').text)
    print num
    sum = sum+num
    print sum

# print output
print sum