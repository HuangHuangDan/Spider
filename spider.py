# -*-coding:utf-8 -*-   

import bs4
import re
import urllib.request, urllib.error, urllib.parse
import sqlite3
import xlwt
from bs4 import BeautifulSoup


def main():
    baseurl = 'https://movie.douban.com/top250?start='
    datalist = getdata(baseurl)
    # savepath = '.\\test2.xls'
    dbpath = 'movies.db'
    # savedata(datalist,savepath)
    savedata2(datalist,dbpath)

    # askURL("https://movie.douban.com/top250?start=")

findlink = re.compile(r'<a href="(.*?)">')   # create regular object, denote regular(str's mode)
findimg = re.compile(r'<img.*src="(.*?)"',re.S) 
findtitle = re.compile(r'<span class="title">(.*?)</span>') 
findrating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findjudge = re.compile(r'<span>(\d*)人评价</span>')
findinq = re.compile(r'<span class="inq">(.*)</span>')
findbd = re.compile(r'<p class="">(.*)</p>',re.S)


def getdata(baseurl):
    datalist = []
    for i in range(0, 5):
        url = baseurl + str(i*25)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser") 
        for item in soup.find_all('div', class_ = "item"):
            data = []
            item = str(item)
            
            link = re.findall(findlink,item)[0]
            data.append(link)

            img = re.findall(findimg,item)[0]
            data.append(img)

            title = re.findall(findtitle,item)
            if (len(title) == 2):
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace("/","")
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(' ')
            
            rating = re.findall(findrating,item)[0] 
            data.append(rating)

            judge = re.findall(findjudge,item)[0]
            data.append(judge)   

            inq = re.findall(findinq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)   
            else:
                data.append(" ")   
            
            bd = re.findall(findbd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ", bd)
            bd = re.sub('/', " ", bd)
            data.append(bd.strip())
            
            datalist.append(data)
            print(datalist)
    return datalist

    


def savedata(datalist, savepath):
    book = xlwt.Workbook(encoding = "utf-8",style_compression=0)
    sheet = book.add_sheet("douban movies",cell_overwrite_ok=True)
    col = ("link","img","name","foreign name","rating","judge","inq","bd")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 125):
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])

    book.save(savepath)



# def savedata2(datalist, savepath):
#     book = xlwt.Workbook(encoding = "utf-8",style_compression=0)
#     sheet = book.add_sheet("douban movies",cell_overwrite_ok=True)
#     col = ("link","img","name","foreign name","rating","judge","inq","bd")
#     for i in range(0, 8):
#         sheet.write(0, i, col[i])
#     for i in range(0, 125):
#         data = datalist[i]
#         for j in range(0, 8):
#             sheet.write(i+1, j, data[j])

#     book.save(savepath)

def init_db(dbpath):
    sql = '''create table movies(
        id integer primary key aotoincrement,
        link text,
        pic text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numerate,
        instroduction text,
        info text
    );
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()




def askURL(url):
    head = {"User-Agent":" Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36"}
    request = urllib.request.Request(url, headers = head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html



if __name__ == "__main__":
    init_db(dbpath)
    print("dsgjkkrg")
    main()



















# import re
# from urllib.parse import urljoin

# import bs4
# import requests

# links_set = set()

# def main():
#     headers = {'user-agent': 'Baiduspider'}
#     base_url = 'https://www.zhihu.com/'
#     resp = requests.get(urljoin(base_url, 'explore'), headers=headers)
#     soup = bs4.BeautifulSoup(resp.text, 'lxml')
#     href_regex = re.compile(r'^/question')
    
#     for a_tag in soup.find_all('a', {'href': href_regex}):
#         if 'href' in a_tag.attrs:
#             href = a_tag.attrs['href']
#             full_url = urljoin(base_url, href)
#             links_set.add(full_url)
#     print('Total %d question pages found.' % len(links_set))
#     print(links_set)

# main()






# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36"}

# url = "https://douban.com"
# data = bytes(urllib.parse.urlencode({"name":"eric"}),encoding = "utf-8")
# req = urllib.request.Request(url = url, headers = headers) 
# response = urllib.request.urlopen(req)
# print(response.read().decode('utf-8'))

