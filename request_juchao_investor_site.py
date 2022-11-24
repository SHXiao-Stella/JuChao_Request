### Author: Stella
### request the data from the website http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search

### this code can be directly used to obtain the investor research information.
### you can also use the updated information in "query" to obtain the public report/regulatory information.

##import
import time
import re
import requests

#the path to store your files
saving_path='I:\\调研数据\\2019q2'

#define the request function
def obtain_and_download_flie(pageNum):
    url='http://www.cninfo.com.cn/new/hisAnnouncement/query'  ##check-network-query-Headers-General-Request URL
    pageNum=int(pageNum)
    ##check-network-query-Payload
    data={'pageNum':pageNum,
        'pageSize':30,
        'column':'szse',
        'tabName':'relation',
        'plate':'',
        'stock':'',
        'searchkey':'',
        'secid':'',
        'category':'', #if you want to download the report with clear type, you should focus on this tag
        'trade':'',
        'seDate':'2019-04-01~2019-06-30', #time
        'sortName':'',
        'sortType':'asc',
        'isHLtitle':'true'}
    ##check-network-query-Headers-General-Request Headers
    headers={'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,sv;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'170',  #sometimes this parameter will change
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'www.cninfo.com.cn',
        'Origin':'http://www.cninfo.com.cn',
        'Referer':'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}
    r=requests.post(url,data=data,headers=headers)
    # Get the report information in json.
    result=r.json()['announcements']

#download
    for i in result:
        if re.search('摘要',i['announcementTitle']):#Avoid downloading some unnecessary documents
            pass
        else:
            title=i['announcementTitle']
            # make sure you have the correct file name
            title=title.replace('*','').replace('/','').replace('?','').replace(':','').replace('|','').replace('"','')
            secName=i['secName']
            secName=secName.replace('*','').replace('/','').replace('?','').replace(':','').replace('|','').replace('"','')
            secCode=i['secCode']
            adjunctUrl=i['adjunctUrl']
            down_url='http://static.cninfo.com.cn/'+adjunctUrl
            # make sure you can download the original file
            if re.search('DOC',i['adjunctType']):
                filename = f'{secCode}{secName}{title}.doc'
            elif re.search('DOCX',i['adjunctType']):
                filename = f'{secCode}{secName}{title}.docx'
            else:
                filename=f'{secCode}{secName}{title}.pdf'
            filepath=saving_path+'\\'+filename
            r=requests.get(down_url)
            with open(filepath,'wb') as f:
                f.write(r.content)
            print(filename,pageNum,'done')
            # Avoid being blocked by the server
            # time.sleep(1)


time_start=time.time()

#it seems that the max number of page is 100.
for pageNum in range(1,101):
    obtain_and_download_flie(pageNum)
time_end=time.time()

print('time cost',time_end-time_start,'s')