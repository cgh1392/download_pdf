from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import shutil
from multiprocessing import Pool
import os
import sys

# TODO : workshop papers

try : target = sys.argv[1]
except : target = "ICCV2019" #change target if you want : ICCV{year} or CVPR{year}

print('accessing cvf open access of '+target)
A = requests.get(url="http://openaccess.thecvf.com/"+target+".py")
soup = bs(A.text)
L = soup.select("#content > dl")[0].findAll("dd")

print(target+ ' paper list crawled')

folder = target+"/"

try:
    os.makedirs(folder)
except FileExistsError:
    # directory already exists
    pass

name_list = [L[2 * i + 1].find("div", class_="bibref").text.split("title = {")[1].split("}")[0] for i in range(int(len(L)/2))]
with open(folder+'_name_list.txt','w', encoding='utf-8') as f :
    f.write("\n".join(name_list))

def download(i):
    url = (
        "http://openaccess.thecvf.com/"
        + L[2 * i + 1].find("a")["href"]
    )
    file_name = (
        L[2 * i + 1]
        .find("div", class_="bibref")
        .text
    )
    file_name = file_name.split("title = {")[1].split("}")[0]
    for c in list('\/:*?"<>|'):
        file_name = file_name.replace(c, "!")
    file_name = folder + file_name + ".pdf"
    with urllib.request.urlopen(url) as response, open(file_name, "wb") as out_file:
        data = response.read()  # a `bytes` object
        out_file.write(data)


if __name__ == '__main__':
    

    
    pool = Pool(processes = 8)
    pool.map(download,range(int(len(L)/2)))
