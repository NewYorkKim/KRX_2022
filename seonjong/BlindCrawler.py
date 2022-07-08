from bs4 import BeautifulSoup, BeautifulStoneSoup
import requests
import re
import pandas as pd
import numpy as np
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import warnings
warnings.filterwarnings('ignore')

url = "https://www.teamblind.com/kr/topics/주식·투자"
class BlindCrawler:
    def __init__(self):
        
        self.url = "https://www.teamblind.com/kr/topics/주식·투자"
        
    def __str__(self):
        print(f"""블라인드는 오늘 게시물일 경우 'xx시간',
              어제 게시물일 경우 '어제',
              2일전부터 7일 전까지는 'x일전',
              그 이후는 mm-dd을 출력합니다.
              따라서 크롤링 전에 오늘 날짜를 확인해야 합니다.
              오늘은 {datetime.datetime.today().date()}입니다.""")
        print("""블라인드 url 기준 :
              1. 띄어쓰기를 '-'로 대체한다.
              2. 특수기호를 제거하는데 기준이 다 다르므로 함부로 re를 통해 제거해서는 안된다.
              ~, (, ), /, , , ., .. 등 특수기호 제거([,], =, -, ㅡ, ♡ 등 은 살림
              !, ?은 갯수에 상관없이 전체 제거, .은 3개 이상부터는 살림""")
        

    def url_crawler(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        driver.maximize_window()

        time.sleep(1)

        cnt = 10000
        while cnt:
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            cnt -= 1
            if type(100 - (cnt // 100)) == int:
                print(100 - (cnt // 100), "퍼센트 진행중")
                
        bs_obj = BeautifulStoneSoup(driver.page_source)
        div = bs_obj.find('div', {'class': 'article-list '})
        posts = div.find_all('div', {'class' : 'tit'})
        posts_title = []
        for t in posts:
            try:
                posts_title.append(t.find('a').find('span').decompose().text.strip())
            except:
                posts_title.append(t.find('a').text.strip())
        posts_href = []
        for l in posts:
            tmp = l.find('a')['href']
            posts_href.append(tmp[tmp.rfind('-'):])
        posts_title = [re.sub(r'[~()%":\'/,!?]', '', i).replace(' ', '-').replace('\n', '') for i in posts_title]

        root_path = "https://www.teamblind.com/kr/post/"
        list_url = list()
        list_url2 = list()
        cnt = 0
        print('처리 들어간다')
        for title, link in zip(posts_title, posts_href):
            # cnt += 1
            title2 = re.sub('[.]', '', title)
            list_url.append(root_path + title + link)
            list_url2.append(root_path + title2 + link)
        tmp = pd.DataFrame({'url_raw' : list_url, 'url' : list_url2})
        tmp.to_csv('url주소들')
        driver.quit()

class BlindPostCrawler:
    def __init__(self):
        print('블라인드 게시물 크롤링을 시작합니다.')
    
    def post_crawler(self):
        urls = pd.read_csv('urls.csv')
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://www.google.co.kr/?client=safari&channel=ipad_bm')
        driver.maximize_window()
        data = []
        for i, url in enumerate(urls['url']):
            if i > 9000:
                print(url, i)
                driver.execute_script(f'window.open("{url}");')
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)

                bs_obj = BeautifulStoneSoup(driver.page_source)
                title = bs_obj.find('div', {'class' : 'article-view-head'})
                main = bs_obj.find('div', {'class' : 'article-view-contents'})
                like = bs_obj.find('div', {'class' : 'article_info'})
                comment = bs_obj.find('div', {'class' : 'article-comments'})
                try:
                    ti = title.find('h2').text # 제목
                    da = title.find('span', {'class' : 'date'}).text.replace('작성일', '') # 날짜
                    if '일' in da:
                        tmp = int(da.replace('일', ''))
                        da = (datetime.datetime.today().date() - datetime.timedelta(days = tmp)).strftime('%m-%d')

                    lo = title.find('span', {'class' : 'pv'}).text.replace('조회수', '') # 조회수

                    tmp = main.find('p', {'class' : 'contents-txt'}).text # 본문
                    try:
                        tmp = tmp[:tmp.index('  ')]
                    except:
                        pass

                    try:
                        li = like.find('a', {'class' : 'like'}).text.replace('좋아요', '') # 좋아요 수
                        if not li:
                            li = 0
                    except:
                        li = 0

                    cc = comment.find('h3').text.replace('댓글 ', '') # 댓글 갯수

                    if '0' in cc: # 댓글
                        co = 0
                    else:
                        co = ''
                        for c in comment.find_all('p', {'class' : 'cmt-txt'}):
                            c = c.text
                            try:
                                co += (c[:c.index('작성일')] + '\n')
                            except:
                                co += (c + '\n')

                    dict_data = {'date':da, 'title' : ti, 'main' : tmp, 'comments' : co,
                            """_summary_
                            """                             'looks_count' : lo, 'likes_count' : li, 'comments_count' : cc}
                    print(dict_data)
                    data.append(dict_data)
                except:
                    dict_data = {'date':None, 'title' : None, 'main' : None, 'comments' : None,
                                'looks_count' : None, 'likes_count' : None, 'comments_count' : None}
                    data.append(dict_data)
                time.sleep(1)
                driver.close()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                if i % 1000 == 0:
                    tmp_df = pd.DataFrame(data)
                    tmp_df.to_csv(f'Blind_{i//1000}.csv')
                    data = []
        tmp_df = pd.DataFrame(data)
        tmp_df.to_csv(f'Blind_last.csv')
        data = []

b = BlindPostCrawler()
b.post_crawler()

while True:
    pass
