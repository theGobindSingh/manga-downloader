import time
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

print("Enter 1 for Desktop <Default> ")
print("Enter 2 for Documents")
print("Enter 3 for Downloads")
print("Enter 4 for Pictures")
print("NOTE: Find will be named same as Manga.")
locationInput = input("[+] Where do you want to download? : ")
saveLOC = "Desktop"
if locationInput == "2":
    saveLOC = "Documents"
elif locationInput == "3":
    saveLOC = "Downloads"
elif locationInput == "4":
    saveLOC = "Pictures"
else:
    saveLOC = "Desktop"

# main_URL = 'https://kissmanga.org/manga/manga-ne990713'
print("\nManga URL example: https://kissmanga.org/manga/manga-ne990713\n")

main_URL = input("[+] Enter the manga URL (only kissmanga.org) : ")

if "https://kissmanga.org/manga" not in main_URL:
    print("\nWRONG INPUT!!! Exiting the program.")
    time.sleep(3)
    exit()

mainHTML = BeautifulSoup(requests.get(main_URL).text, "lxml")

chapter_pre_URL = 'https://kissmanga.org'

try:
    mangaName = mainHTML.find(
        "div", {"class": "bigBarContainer full"}).find("h2").text
except:
    mangaName = "manga_downloader"

# print(mangaName) #perfectly working

path_saveDown = os.path.join(os.path.join(os.path.join(
    os.path.expanduser('~')), saveLOC), mangaName)  # Downloading Images Folder
if not os.path.exists(path_saveDown):
    os.mkdir(path_saveDown)

# chapterListTemp = mainHTML.find("div",{"class":"listing listing8515 full"}).find_all("div")
chapterListTemp = mainHTML.select(".listing.listing8515.full > div")

chapterList = []

for i in range(1, len(chapterListTemp)):
    # temp = chapterListTemp[i].find("a").get_text().split("-")[-1].replace("  ","").replace("\n","").replace("Chapter ","")
    # if " " in temp:
    #     temp = temp.split()[0]
    # if ":" in temp:
    #     temp = temp.replace(":","")
    temp = chapterListTemp[i].find(
        "a").get_text().replace("  ", "").replace("\n", "")
    chapterList.append({"name": temp, "url": chapter_pre_URL +
                       ""+chapterListTemp[i].find("a").attrs["href"]})

chapterList.reverse()

print("\nChapter List: \n")
for i in range(1, len(chapterList)+1):
    print(str(i)+": "+chapterList[i-1]["name"])

startChapter = input(
    "[+] Enter the starting number (must be greater or equal to 1)\n: ")
endChapter = input(
    "[+] Enter the starting number (must be lesser or equal to "+str(len(chapterList))+")\n: ")

try:
    startChapterIndex = int(startChapter)-1
    endChapterIndex = int(endChapter)-1
    if startChapterIndex < 0:
        startChapterIndex = 0
    if endChapterIndex >= len(chapterList):
        endChapterIndex = len(chapterList)-1
except:
    startChapterIndex = 0
    endChapterIndex = len(chapterList)-1

for i in range(startChapterIndex, endChapterIndex+1):
    chapter = chapterList[i]["name"].replace("Chapter", " Chapter").replace("chapter", " chapter").replace("\\", "_").replace("/", "_").replace(
        ":", " - ").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("-", " - ")
    link = chapterList[i]["url"]
    chapterHTML = BeautifulSoup(requests.get(link).text, "lxml")
    allImgElems = chapterHTML.find(
        "div", {"id": "centerDivVideo"}).findAll("img")
    imgLinks = []
    for j in allImgElems:
        imgLinks.append(j.attrs["src"])
    chapterPath = os.path.join(path_saveDown, chapter)
    if not os.path.exists(chapterPath):
        os.mkdir(chapterPath)
    # progress_bar = tqdm(range(1,len(imgLinks)),unit="%",unit_scale=True,bar_format="{l_bar}{bar}| [{elapsed}]",postfix="")
    print("Downloading "+chapter+"... Please wait...")
    for j in tqdm(range(1, len(imgLinks)), unit="%", unit_scale=True, bar_format="{l_bar}{bar}| [{elapsed}]", postfix=""):
        currentImgLink = imgLinks[j-1]
        response = requests.get(currentImgLink, stream=True)
        imgType = (response.headers['content-type']).split("/")[-1]
        with open(os.path.join(chapterPath, (str(j)+"."+imgType)), "wb+") as file:
            file.write(response.content)
            file.close()
