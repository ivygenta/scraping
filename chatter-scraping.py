# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
import dao

#--------readme-----------------------
#最初の実行時は携帯認証の画面が表示されるので手動で認証してやりなおす、二回目以降は認証不要のはず
#※何回も携帯認証すると認証ロックするみたいなので気を付ける
#iniファイルを書き換えてプロジェクトフォルダ直下におく
#--------readme-----------------------

#iniファイル読み込み
inifile = configparser.ConfigParser()
inifile.read('./config.ini', 'UTF-8')

#headless モード
#options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#,options=options(有効にするときはこれをdriveroptionに追加)

#user-data-dir指定(chromeのuser情報格納場所を指定)
usoptions = webdriver.ChromeOptions()
usoptions.add_argument('--user-data-dir='+inifile.get('chrome', 'user-data-dir'))

#webdriver初期化
driver = webdriver.Chrome(executable_path=inifile.get('chrome', 'chromedriverpath'),options=usoptions)
driver.get('https://login.salesforce.com/?locale=jp')

#ログイン処理
def login():
 username = driver.find_element_by_name("username")
 password = driver.find_element_by_name("pw")
 username.send_keys(inifile.get('user', 'username'))
 password.send_keys(inifile.get('user', 'pw'))
 username.submit()

#「表示件数を増やす」押下する処理
def morebottunpush():
 delay = 10 # seconds
 WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, '更新の表示件数を増やす »')))#ボタンが表示されるまで待つ
 driver.find_element_by_link_text('更新の表示件数を増やす »').click()

#画面スクロールで読み込まれる情報を表示する処理
def scroll():
 for i in range(100):
       time.sleep(2)#読み込みを待つ
       driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")#下までスクロールする

       #特定のクラスに「ダウンロード中」の文字があれば繰り返す
       #「ダウンロード中」：あったら続行、なければ終了
       sc = driver.find_elements_by_xpath("//*[@class='cxshowmorefeeditemscontainer showmorefeeditemscontainer']")
       for scc in sc:
        b = "false"
        if "ダウンロード中" in scc.text:
         b = "true"
       if  "true" in b:
        continue
       else:
          break

#さらに表示リンクを押しまくる処理
def morebottuns():
 cxmore = driver.find_elements_by_xpath("//*[@class='cxmorelink']")
 for more in cxmore:
     more.click()


#特定の文字で投稿を検索する処理
def serch():
 textelements = driver.find_elements_by_xpath("//*[@class='feeditemtext cxfeeditemtext']")
 print(textelements)
 commentlist = []
 for ele in textelements:
     if inifile.get('search', 'searchword') in ele.text:
           commentlist.append(ele.text)
           print(ele.parent)
           print(ele.text)
           print("------投稿区切り-------")

 dao.insertsql(commentlist)

login()
morebottunpush()
scroll()
morebottuns()
serch()
driver.quit()


