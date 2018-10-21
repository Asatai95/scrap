
"""
pip install beautifulsoup4
pip install selenium
pip install tqdm
参考リンク
Python Webスクレイピング 実践入門
https://qiita.com/Azunyan1111/items/9b3d16428d2bcc7c9406
PythonとBeautiful Soupでスクレイピング
https://qiita.com/itkr/items/513318a9b5b92bd56185
Python Webスクレイピング テクニック集「取得できない値は無い」JavaScript対応@追記あり6/12
https://qiita.com/Azunyan1111/items/b161b998790b1db2ff7a
Webスクレイピングの注意事項一覧
https://qiita.com/nezuq/items/c5e827e1827e7cb29011
１．コネタ一覧ページのURLセット
２．コネタ記事の全ての「タイトル」と「リンク」を取得

"""

from datetime import datetime
now = datetime.now()
THIS_YEAR = now.year
THIS_MONTH = now.month

from time import sleep
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 進捗バー表示用
from tqdm import tqdm

"""
1 URL をセット
"""
DOKI_KONETA = 'https://www.dee-okinawa.com/koneta/'


"""
2
# start 2014/04/
# end   2018/10/
"""

# 小ネタ一覧ページのリンクを格納
koneta_urls = []

# 小ネタ一覧ページのリンクを 年月別に生成していく
# 例 https://www.dee-okinawa.com/koneta/2014/04/
# 2014年から2018年までの記事を取得
for year in range(2014, THIS_YEAR+1):
  # 1月から12月まで
  for month in range(1, 13):

    # 2014年は４月からスタートしているので3月まではスキップ
    if year == 2014 and month <= 3:
      continue

    # フォーマット調整 -> 2014/01/, 2014/12/
    # 1桁の数字は前に0が入る
    if month <= 9:
      target = '%s/0%s/' %(year, month)
    else:
      target = '%s/%s/' %(year, month)

    # 年月の文字列をフォーマットしたあとに小ネタリンクと結合
    # 結合後、リストへ追加
    # このリストは次のステップで使用する
    koneta_urls.append(DOKI_KONETA+target)

    # 今月になったらリンク生成終了
    if year == THIS_YEAR and month == THIS_MONTH:
      break

"""
3
取得したリンクをもとにアクセスしてほしい情報をとる
２次元リスト
koneta_links = [
  ['https://www.dee-okinawa.com/koneta/2014/04/mozuku.html', 'https://www.dee-okinawa.com/koneta/2014/04/math.html', 'https://www.dee-okinawa.com/koneta/2014/04/don.html', 'https://www.dee-okinawa.com/koneta/2014/04/slide.html', 'https://www.dee-okinawa.com/koneta/2014/04/tougan2014.html', 'https://www.dee-okinawa.com/koneta/2014/04/kusshi.html'],
]
２次元リスト
koneta_titles = [
  ['モズクの日に行なわれたもずくのテープカットとは', '「沖縄の算数ものがたり」が割とマニアック', 'さようならどん亭開南店', '直角すべり台の滑降速度はどれぐらいなのか？', '冬瓜（とうがん）は本当に冬まで持つのか2014', '名護市にいるあのキャラクターの名前が判明', '月別で見る'],
]
２次元リスト
koneta_date = [
  ['2014.04.24', '2014.04.22', '2014.04.17', '2014.04.15', '2014.04.10', '2014.04.08'],
]
２次元リスト > Dictionary
koneta_socials = [
  [{'facebook': '210', 'twitter': '10'}, {'facebook': '582', 'twitter': '32'}, {'facebook': '848', 'twitter': '57'}, {'facebook': '278', 'twitter': '20'}, {'facebook': '169', 'twitter': '12'}, {'facebook': '239', 'twitter': '10'}]
]
"""


# 取得したデータを格納するリスト
koneta_links = []
koneta_titles = []
koneta_date = []
koneta_socials = []


# 前のステップで生成した小ネタ一覧ページのリンクの数だけループさせる
# count 今何回目か判断するもの. リンクが１０個なら 0 スタート 9 エンド
# url 小ネタのリンクが入っている
for count, url in enumerate(koneta_urls):
  print(count+1,'/'+ str(len(koneta_urls)) +'回目')

  """
  ########### 注意 ###########
  アクセスしたあとは１秒スリープさせる
  """
  # ????年??月の小ネタ一覧ページへアクセス
  html = urllib.request.urlopen(url)
  sleep(1)

  # アクセスしたリンクを分析する
  soup = BeautifulSoup(html, "html.parser")

  # 各年月の小ネタ一覧ページのタイトルを取得

  # 一時的に必要なリスト なので変数名の前に tmp がついている.　temporaryの略
  tmp_titles = []

  # ????年??月の小ネタ一覧ページｈにアクセスして取得したDOMから h2 を全県取得
  for h2 in soup.find_all('h2'):

    # 取得した h2 からテキストだけ取得
    tmp_titles.append(h2.get_text())
    # 中身は下記のように増えていく
    # ['タイトル１']
    # ['タイトル１', 'タイトル2']

  # "月別で見る" というタイトルが最後に入るので削除
  tmp_titles.pop()

  # 取得したタイトルをリストに追加
  koneta_titles.append(tmp_titles)
  # ↑の中身は下記のように増えていく
  # [['タイトル１', 'タイトル2']]
  # [['タイトル１', 'タイトル2'], ['タイトル１', 'タイトル2']]
  # [['タイトル１', 'タイトル2'], ['タイトル１', 'タイトル2'], ['タイトル１', 'タイトル2']]

  # 一時的な変数なので削除
  del tmp_titles

  # 各年月の小ネタ一覧ページのリンクを取得

  # 一時的に link を格納するリスト
  tmp_links = []

  # アクセスした小ネタ記事一覧から個別タイトルのリンクを取得する
  for li in soup.select('ul.contentsList > li'):

    # aタグから href 属性のテキストを取得する
    tmp_links.append(li.find('a').get('href'))

  #取得したリンクをリストに追加
  koneta_links.append(tmp_links)
  # ↑の中身は下記のように増えていく
  # [['リンク１', 'リンク2']]
  # [['リンク１', 'リンク2'], ['リンク１', 'リンク2']]
  # [['リンク１', 'リンク2'], ['リンク１', 'リンク2'], ['リンク１', 'リンク2']]


  # 一時的な変数なので削除
  del tmp_links

  # ちゃんと取得できているか確認用にプリント
  # print(koneta_links)



  # 一時的な変数
  tmp_koneta_socials = []
  tmp_koneta_date = []


  # tqdm を使うと実行中にステータスバーが出るので進捗が見やすい
  for num, koneta_link in enumerate(tqdm(koneta_links[count])):

    # javascript経由でアクセセスするために selenium を使用
    # set_headless True はブラウザの起動をオフにしている
    options = Options()
    options.set_headless(True)

    # mac の方はこちら
    driver = webdriver.Chrome(chrome_options=options)

    # windows の方はこちら
    # download必須 http://chromedriver.chromium.org/downloads
    # download したら .exe ファイルを同じフォルダのなかに
    # driver = webdriver.Chrome(
    #   chrome_options=options,
    #   executable_path='./chromedriver.exe'
    # )

    """
    ########### 注意 ###########
    アクセスしたあとは１秒スリープさせる
    """
    # 小ネタ記事には javascript 対応させるために selenium 経由
    driver.get(koneta_link)
    sleep(1)

    # アクセスしたリンクを分析する
    konetahtml = driver.page_source.encode('utf-8')
    konetasoup = BeautifulSoup(konetahtml, "html.parser")


    # 日付をリストに格納
    tmp_koneta_date.append(
      # 日付取得
      konetasoup.select_one('#contents > article > div > div > div.articleHeader > div.l > div').get_text()
    )

    # それぞれのiframeのURLを取得
    # twitter は http: が抜けているので自分で追加
    facebookiframe_url = konetasoup.select_one('#contents > article > div > div > ul > li.fb > div > span > iframe').get('src')
    twitteriframe_url = 'http:' + konetasoup.select_one('#twitter-widgetoon-0').get('src')

    # facebook いいね数のリンクにアクセス
    facebookhtml = urllib.request.urlopen(facebookiframe_url)

    # tweet 数のリンクにアクセス
    # javascriptに対応させるため selenium 経由
    driver.get(twitteriframe_url)
    twitterhtml = driver.page_source.encode('utf-8')

    # それぞれアアクセスしたリンクを分析する
    facebookhtmlsoup = BeautifulSoup(facebookhtml, "html.parser")
    twitterhtmlsoup = BeautifulSoup(twitterhtml, "html.parser")

    # それぞれほしいデータを取得する
    # facebook いいね数
    # twitter ツイート数
    facebook_like = facebookhtmlsoup.select_one('#u_0_1').get_text()
    tweet_count = twitterhtmlsoup.select_one('#count').get_text()

    # 取得したデータの格納
    tmp_koneta_socials.append(
      {
        'facebook': facebook_like,
        'twitter': tweet_count,
      }
    )

    # print(tmp_koneta_date)

  koneta_date.append(tmp_koneta_date)
  koneta_socials.append(tmp_koneta_socials)

  # 上記は以下のうように増えていく
  # koneta_date
  # [['日付１', '日付２']]
  # [['日付１', '日付２'], ['日付１', '日付２']]
  # [['日付１', '日付２'], ['日付１', '日付２'], ['日付１', '日付２']]
  # koneta_socials
  # [[{'facebook':'111', 'twitter':'111'}, {'facebook':'111', 'twitter':'111'}]]
  # [[{'facebook':'111', 'twitter':'111'}, {'facebook':'111', 'twitter':'111'}], [{'facebook':'222', 'twitter':'222'}, {'facebook':'222', 'twitter':'222'}]]

  # 一時的なので削除
  del tmp_koneta_date
  del tmp_koneta_socials


"""
CSVへ出力処理
koneta_links
koneta_titles
koneta_date
koneta_socials
参考
PythonでCSVファイルの読み込み・書き込みを行う方法
https://uxmilk.jp/8693
PythonでCSVの読み書き
https://qiita.com/okadate/items/c36f4eb9506b358fb608
Pythonでファイルの読み込み、書き込み
https://note.nkmk.me/python-file-io-open-with/
"""

print('CSV書き込みスタート')

import csv

# CSV の１行目のカラム名用
header = ['日付', 'タイトル','facebook_いいね', 'twitter_ツイート', 'url']


# with ブロックを使うとファイル書き込み終了後に自動で閉じてくれる
with open('deeokinawa_koneta.csv', 'w') as f:

    # CSV を書き込むオブジェクトセット
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく

    # 1行目はカラム名
    writer.writerow(header)

    # ２行目以降はこれまで取得したデータをで書き込んでいく

    # 取得した koneta_links の数だけ for文 を回す
    for count in range(0, len(koneta_links)):

      # 記事一覧ページにアクセスしたときに タイトルの数だけ for文 を回す
      for count_title in range(0, len(koneta_titles[count])):
        tmp = [
          koneta_date[count][count_title],# 日付
          koneta_titles[count][count_title],# タイトル
          koneta_socials[count][count_title]['facebook'],# facebook いいね数
          koneta_socials[count][count_title]['twitter'],# twitter ツイート数
          koneta_links[count][count_title],# url
        ]

        # 書き込んでいる内容を出力確認用にプリント
        print(tmp)

        # 書き込み
        writer.writerow(tmp)

        # 一時的なので削除
        del tmp
