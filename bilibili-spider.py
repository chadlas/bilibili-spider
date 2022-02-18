"""

m4s 是视频或者音频的资源

通过浏览器的抓包发现，视频的加载流程：
1、访问到主页面，能拿到的是页面源代码，目的是拿到M4S的地址
2、访问到M4S地址
3、下载和保存

#https://upos-sz-mirrorkodo.bilivideo.com/upgcxcode/16/00/270940016/270940016-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1638415453&gen=playurlv2&os=kodobv&oi=2574692664&trid=5cf56081738b45fea28ffbed4ed92589u&platform=pc&upsig=a7fe6c3616ef9d17a38f5c546c2e5d50&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=296478422&bvc=vod&nettype=0&orderid=0,3&agrr=0&bw=330415&logo=80000000
#https://upos-sz-mirrorkodo.bilivideo.com/upgcxcode/16/00/270940016/270940016-1-30077.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1638415453&gen=playurlv2&os=kodobv&oi=2574692664&trid=5cf56081738b45fea28ffbed4ed92589u&platform=pc&upsig=2e2117e93b6809b31cdba3a666a08b85&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=296478422&bvc=vod&nettype=0&orderid=0,3&agrr=0&bw=198591&logo=80000000
"""
import os
import re
import json
import requests
from lxml import etree

def download_B(bv):
    # url = input("请输入视频地址：")
    # name = input("请输入视频名字：")
    main_page = f"https://www.bilibili.com/video/{bv}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    resp = requests.get(main_page, headers=headers) # verify=False
    # print(resp.text)

    tree = etree.HTML(resp.text)
    name = tree.xpath("//title/text()")[0]

    # 从页面代码中提取部分代码，使用re，正则
    # 提取规则  # 正则中 . 默认不能匹配换行，加上re.S 可以匹配换行

    obj = re.compile(r"window.__playinfo__=(?P<play_info>.*?)</script>")
    r = obj.search(resp.text, re.S)
    play_info = r.group("play_info")
    # print(play_info)   # play_info是字符串
    # 正则是在一大堆字符串中提取数据，因此提取到的数据也是字符串

    # 接下来从play_info中提取视频的下载地址
    # 需要把json字符串转化成python中的字典

    play_info_dic = json.loads(play_info)  # 可以把字符串转成字典
    video_url = play_info_dic['data']['dash']['video'][0]['baseUrl']
    audio_url = play_info_dic['data']['dash']['audio'][0]['baseUrl']
    # print(video_url)

    # 下载视频
    headers['referer'] = main_page
    resp = requests.get(video_url, headers=headers)
    with open("temp_video.m4s", mode="wb") as f:
        f.write(resp.content)

    # 下载音频
    headers['referer'] = main_page
    resp = requests.get(audio_url, headers=headers)
    with open("temp_audio.m4s", mode="ab") as f:
        f.write(resp.content)

    # 使用ffmpeg将视频和音频进行合并
    os.system(f"ffmpeg -i temp_audio.m4s -i temp_video.m4s -codec copy {name}.mp4")
    # os.system(f"ffmpeg -i temp_audio.m4s -i temp_video.m4s -codec copy '{name}.mp4'")
    os.remove("temp_audio.m4s")
    os.remove("temp_video.m4s")
    print("下载成功！！！" , name)

if __name__ == '__main__':
    a = input("请输入要获取B站的BvID:")
    download_B(a)


