from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import shutil
from multiprocessing import Pool
import os

target = "ICCV2019"
A = requests.get(url="http://openaccess.thecvf.com/"+target+".py")
soup = bs(A.text)
L = soup.select("#content > dl")[0].findAll("dd")

folder = target+"/"

try:
    os.makedirs(folder)
except FileExistsError:
    # directory already exists
    pass


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
