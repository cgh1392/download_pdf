from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import shutil
import os
from multiprocessing import Pool

year = 2019
url = 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-{}-{}'.format(year+13-2000,year) # {year+13}-{year}
A = requests.get(url=url) 
soup = bs(A.text)

L = [[i.contents[0]['href'],i.contents[0].contents[0]] for i in soup.select('body > div.main-container > div > ul')[0].findAll('li')]



def download(i):
    url = (
        'https://papers.nips.cc'+L[i][0]+'.pdf'
    )
    file_name = (
        L[i][1]
    )
    folder = '2019/'
    for c in list('\/:*?"<>|'):
        file_name = file_name.replace(c, "!")
    file_name = folder + file_name + ".pdf"
    if os.path.exists(file_name) : return
    with urllib.request.urlopen(url) as response, open(file_name, "wb") as out_file:
        data = response.read()  # a `bytes` object
        out_file.write(data)



if __name__ == '__main__':
    

    
    pool = Pool(processes = 8)
    pool.map(download,range(len(L)))
