#-------------------------------------------------------------------------------
# Name:        imageScraper
# Purpose:
#
# Author:      Joakim
#
# Created:     07.06.2014
# Copyright:   (c) Joakim 2014
#-------------------------------------------------------------------------------
"""
A script that downloads the images from a spesific japanese imageboard
and saves them in a separate folder for each thread parsed.
"""

import urlparse
import urllib, re,os, urllib2
from bs4 import BeautifulSoup

#changes a link with japanese kanji to encoded url
def convertJapURLEncoded(url):
    print url
    complete=urlparse.urlsplit(url)
    pathname=complete.query
    #our pathname is equal to the japanese part of the link
    pathname=pathname.replace('name=', "")
    #quote + encode to shift-jis standard
    try:
        urlencoded=urllib2.quote(pathname.encode('shift-jis'))
        url=url.replace(pathname, urlencoded)
        print url
    except:
        print url
    return url

#finds all links in soup matching regex, for which string "checkfor" is a part of
def gothroughStack(stack, soup, regexString,checkfor):
    for link in soup.findAll('a', href=re.compile(regexString)):
        link['href'] = urlparse.urljoin(url, link['href'])
        if checkfor in link['href']:
            stack.append(link['href'])

    return 0

maindir= os.getcwd() + '/test/'

if not os.path.isdir(maindir):
    os.mkdir(maindir)

check = "http://xxxxxxxx.com/test" #image-urls must contain this path
url = "http://xxxxxxxx.com/test/bbs.php" #domain of imageboard, must contain http://

urls = [url]    #Stack of urls to scrape
imgurls = []

htmltext = urllib.urlopen(urls[0]).read()
print(urls[0])
soup = BeautifulSoup(htmltext)


#gets all the links on the given page
gothroughStack(urls,soup,'bbs.php\?name=', url)
print len(urls)


#looks through all pages and adds image-links from all these to imgurls
while len(urls)>0:
    currentUrl = urls.pop()
    usableUrl=convertJapURLEncoded(currentUrl)


    #creates our pathname based on threadname
    pathname=urlparse.urlsplit(currentUrl)
    pathname=pathname.query
    pathname=pathname.replace('name=', "")
    pathname=re.sub(r'[?/.,;:\t]', r'', pathname)
    print(pathname)

    #make make path, make directory, set to current write-directory.
    path = maindir + pathname

    existed=True
    #if-test does directory exist? make dir
    if not os.path.isdir(path):
        os.mkdir(path)
        existed=False

    if not existed:

        try:
            htmltext = urllib.urlopen(usableUrl).read()
        except:
            print(usableUrl)
        soup = BeautifulSoup(htmltext)
        print len(urls)
        #find all pictures start start with '.' ,which are big pics
        gothroughStack(imgurls,soup,'./img/',check)

        print len(urls)


        os.chdir(path)
        while len(imgurls)>0:
            linkToImg = imgurls.pop()
            #if the directory exists from before, we have already downlaoded
            #the images, so we just unload the stack
            if not existed:
                filename = urlparse.urlsplit(linkToImg)
                filename = basename(filename.path)
                image = urllib.urlretrieve(linkToImg, filename)
                print(filename)
                print len(imgurls)

