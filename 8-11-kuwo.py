import requests
import os
from pathlib import Path

singer_name = input('请输入歌手姓名：')
pn = input('请输入歌手页码：')
for a in range(int(pn)):
    b = int(a)+1
    # print(b)
    url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn=30&httpsStatus=1&reqId=e1a0e1e0-dba7-11ea-b293-1f758a66533b'.format(singer_name,b)
    headers = {
        'Cookie':'ga=GA1.2.1591089013.1594703285; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1594703285,1594717407,1597132301; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1597132301; _gid=GA1.2.654870698.1597132302; kw_token=SPP8IRS396P',
        'csrf': 'SPP8IRS396P',
        'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

    }

    response = requests.get(url,headers=headers).json()
    music = response['data']['list']
    # print(music)
    for i in music:
       # print(i["name"])
       # print(i["rid"])
       # print(i)
       url1 = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1597132467977&httpsStatus=1&reqId=e1a2b6a1-dba7-11ea-b293-1f758a66533b'.format(i['rid'])
       music_url = requests.get(url1,headers=headers).json()
       # print(music_url['url'])
       try:
           music_file = Path('music1')
           if not music_file.is_dir():
                os.mkdir('music1')
           else:
               # print('hello word')
               with open('music1/'+singer_name+'--'+i['name']+'.mp3','wb') as f:
                   response = requests.get(music_url['url'],headers=headers)
                   print('正在下载歌曲-----{}'.format(i['name']),end='----->\n')
                   f.write(response.content)
                   f.close()
       except Exception as e:
            print(Exception)
            print('{}下载出错了'.format(i['name']))


    print('第{}页下载结束。。。'.format(b))

print('全部输入页下载结束。。。')