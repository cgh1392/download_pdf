from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import shutil
from multiprocessing import Pool
import os
import sys

try : year = int(sys.argv[1])
except : year = 2019 # change year if you want

print('accessing nips publication website of year '+str(year))
url = 'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-{}-{}'.format(year+13-2000,year) # {year+13}-{year}
A = requests.get(url=url) 
soup = bs(A.text)

L = [[i.contents[0]['href'],i.contents[0].contents[0]] for i in soup.select('body > div.main-container > div > ul')[0].findAll('li')]


print('nips' +str(year)+ ' paper list crawled')
target = 'NIPS'+str(year)
folder = target+"/"

try:
    os.makedirs(folder)
except FileExistsError:
    # directory already exists
    pass

name_list = [i[1] for i in L]
with open(folder+'_name_list.txt','w', encoding='utf-8') as f :
    f.write("\n".join(map(str,name_list)))


def download(i):
    url = (
        'https://papers.nips.cc'+L[i][0]+'.pdf'
    )
    file_name = (
        L[i][1]
    )
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
