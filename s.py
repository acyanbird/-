import requests
from bs4 import BeautifulSoup
import os

link = ['https://mangakakalot.com/manga/moira_2', 'https://mangakakalot.com/manga/shinyaku_marchen', 'https://mangakakalot.com/manga/kyuuyaku_marchen']  # fill in the link that the main page of manga you want to download
ErrorLink = []

def getChapList(MainLink):  # get the link of chapters from main page
    list = []  # store the chapter's link
    r = requests.get(MainLink)
    s = BeautifulSoup(r.text, 'lxml')
    chapter = s.find(class_="chapter-list")
    #print(chapter)
    for link in chapter.find_all('a'):
        list.append(link.get("href"))
    return list

def getImage(ChapLink):  # in one chapter get all the links of images
    list = []
    r = requests.get(ChapLink)
    s = BeautifulSoup(r.text,'lxml')
    image = s.find(class_='vung-doc')
    for im in image.find_all('img'):
        list.append(im.get("src"))
    return list

def writeIm(ImLink):  # write image
    r = requests.get(ImLink)
    with open('%s/%d.jpg' % (CurrentFolder, ImgNum), 'wb')as im:
        im.write(r.content)

for manga in range(len(link)):
    if not os.path.exists('./%s' % link[manga].split('/')[-1]):
        os.mkdir('./%s' % link[manga].split('/')[-1])  # create folder of manga
    ChapList = getChapList(link[manga])  # store Chaplist
    for ChapNum in range(len(ChapList)):  # iteration of chapters
        CurrentChap = getImage(ChapList[ChapNum])
        CurrentFolder = './%s/%s' % (CurrentChap[ChapNum].split('/')[-3], CurrentChap[ChapNum].split('/')[-2])  # create folder for each chapter
        if not os.path.exists(CurrentFolder):
            os.mkdir(CurrentFolder)
        for ImgNum in range(len(CurrentChap)):
            if not os.path.exists('%s/%d.jpg' % (CurrentFolder, ImgNum)):
                writeIm(CurrentChap[ImgNum])



