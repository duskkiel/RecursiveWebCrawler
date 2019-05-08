# Have to run from the command line

import sys
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def getPage(url):
    try:
        import urllib.request
        return urllib.request.urlopen(url).read().decode("utf8")
    except:
        return


def getNextTarget(page):
    if page is None:
        return None, 0

    startLink = page.find('<a href=')

    if startLink == -1:
        return None, 0

    startQuote = page.find('"', startLink)
    startQuote += 1
    endQuote = page.find('"', startQuote)
    url = page[startQuote: endQuote]
    return url, endQuote


def getAllLinks(page):
    links = {''}
    while True:
        url, endpos = getNextTarget(page)
        if url:
            links.add(url)
            page = page[endpos:]
        else:
            break
    return links


def union(p, q):
    for i in q:
        if i not in p:
            p.append(i)


def crawlWeb(seed, maxDepth, depth, crawled):
    if depth > maxDepth:
        return

    tocrawl = {seed}  # List of pages left to crawl
    nextDepth = []  # To keep track of depth # Initial depth

    page = tocrawl.pop()

    if page not in crawled:
        union(nextDepth, getAllLinks(getPage(page)))
        for url in nextDepth:
            if isAbo(url):
                print("\t" * depth, url)
                tocrawl.add(url)
                crawled.add(page)
                crawlWeb(url, maxDepth, depth + 1, crawled)
            else:
                absolute = urlparse(page)
                url = absolute.scheme + "://" + absolute.netloc + url
                if url not in crawled:
                    print("\t" * depth, url)
                    tocrawl.add(url)
                    crawled.add(page)
                    crawlWeb(url, maxDepth, depth + 1, crawled)


def isAbo(url):
    return bool(urlparse(url).netloc)


def main():
    if len(sys.argv) == 2:
        seed = sys.argv[1]
        if isAbo(seed) is False:
            print("Error: [Url doesn't exist or is relative]")
            sys.exit()
        maxDepth = 3
        crawled = {''}
        crawlWeb(seed, maxDepth, 0, crawled)

    elif len(sys.argv) == 3:
        seed = sys.argv[1]
        if isAbo(seed) is False:
            print("Error: [Url doesn't exist or is relative]")
            sys.exit()
        maxDepth = int(sys.argv[2])
        crawled = {''}
        crawlWeb(seed, maxDepth, 0, crawled)

    else:
        print("Error: [Incorrect length of arguments]")


main()
