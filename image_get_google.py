import os
import sys
from urllib import request as req
from urllib import error
from urllib import parse
import bs4

def encode(keyword):
    urlKeyword = ''
    
    # 検索語句のURLをgoogle画像検索用のURLにエンコード
    for word in keyword:
        urlKeyword = parse.quote(word) + '+'

    url = 'https://www.google.com/search?hl=jp&q=' + urlKeyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'

    # GoogleからFireFoxにヘッダを偽装
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
    request = req.Request(url=url, headers=headers)
    
    return req.urlopen(request)

def get_image(keyword):
    html = encode(keyword).read().decode('utf-8')
    html = bs4.BeautifulSoup(html, "html.parser")
    elems = html.select('.rg_meta.notranslate')
    counter = 0
    for ele in elems:
        ele = ele.contents[0].replace('"','').split(',')
        eledict = dict()
        for e in ele:
            num = e.find(':')
            eledict[e[0:num]] = e[num+1:]
        imageURL = eledict['ou']

        pal = '.jpg'
        if '.jpg' in imageURL:
            pal = '.jpg'
        elif '.JPG' in imageURL:
            pal = '.jpg'
        elif '.png' in imageURL:
            pal = '.png'
        elif '.gif' in imageURL:
            pal = '.gif'
        elif '.jpeg' in imageURL:
            pal = '.jpeg'
        else:
            pal = '.jpg'

        try:
            img = req.urlopen(imageURL)
            localfile = open('./'+sys.argv[1]+'/'+sys.argv[1]+str(counter)+pal, 'wb')
            print(imageURL)
            localfile.write(img.read())
            img.close()
            localfile.close()
            counter += 1
        except UnicodeEncodeError:
            continue
        except error.HTTPError:
            continue
        except error.URLError:
            continue`

def main():
    # keywordは２つまで
    for i in [2, 3]:
        if len(sys.argv) == 2:
            keyword = [sys.argv[1]]
        elif len(sys.argv) == 3:
            keyword = [sys.argv[1], sys.argv[2]]
    if len(keyword) <= 0:
        print('keywordが指定されていません')
        exit()
    
    # フォルダの作成
    os.mkdir(sys.argv[1])
    
    get_image(keyword)

if __name__ == '__main__':
    main()