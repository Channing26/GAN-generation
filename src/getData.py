#采用request+beautiful库爬取
import requests
from bs4 import BeautifulSoup
import os
import traceback#python异常模块
import shutil

def download(url, filename):#判断文件是否存在，存在则退出本次循环
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=60)#以流数据形式请求，你可获取来自服务器的原始套接字响应
        r.raise_for_status()
        with open(filename, 'wb') as f:#将文本流保存到文件
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()#把返回信息输出到控制台
        if os.path.exists(filename):
            os.remove(filename)


savedir='../imgs/animes1/'
if os.path.exists(savedir):
    shutil.rmtree(savedir)
    
os.makedirs(savedir)

start = 1
end = 80
for i in range(start, end + 1):
    url = 'http://konachan.net/post?page=%d&tags=' % i#需要爬取的url
    html = requests.get(url).text#获取的html页面内容
    soup = BeautifulSoup(html, 'html.parser')
    cnt=0
    for img in soup.find_all('img', class_="preview"):
        #target_url = 'http:' + img['src']
        target_url = img['src']
        #filename = os.path.join('../imgs', target_url.split('/')[-1])
        filename = savedir+str(i)+"_"+str(cnt)+".jpg"
        cnt=cnt+1
        print(filename)
        download(target_url, filename)
    print('%d / %d' % (i, end))
