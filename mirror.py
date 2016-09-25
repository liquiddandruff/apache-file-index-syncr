#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
from urllib import request
from pathlib import Path

# sorted by descending; new files first
URL = "http://www2.cs.sfu.ca/CourseCentral/471/qgu/Notes/?C=M;O=D"
OUT_DIR = "./notes/"

def main():
    page = request.urlopen(URL)
    pageSoup = bs(page.read(), "html.parser")

    pdfLinks = []
    pdfNames = []
    # get all links after first 5 so we get the files we want
    for link in pageSoup.find_all("a")[5:]:
        full_link = URL + link.get("href")
        if full_link.endswith(".pdf"):
            pdfLinks.append(full_link)
            pdfNames.append(link.get("href"));
            print("pdf: " + full_link);

    pdfZip = zip(pdfNames, pdfLinks)

    pdfsSynced = 0;
    for name, link in pdfZip:
        rq = request.urlopen(link)
        testFile = Path(OUT_DIR + name)
        if testFile.is_file():
            print("Skipping " + name)
            continue
        pdfsSynced = pdfsSynced + 1
        pdfFile = open(OUT_DIR+ name, 'wb')
        pdfFile.write(rq.read())
        pdfFile.close();
    
    print("Synced %d" % pdfsSynced + " pdfs")


if __name__ == "__main__":
    main()

