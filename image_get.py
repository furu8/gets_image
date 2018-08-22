import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup

URL = 'http://re-zero-anime.jp/'
def download_images(url):
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    for link in soup.find_all("img"):
        src_attr = link.get("src")
        print(src_attr)
        # 相対URLから絶対URLに変換
        yield urljoin(URL, src_attr)

def main():
    for target in download_images(URL):
        re = requests.get(target)
        with open('img/' + target.split('/')[-1], 'wb') as f:
            f.write(re.content)

if __name__ == '__main__':
    main()