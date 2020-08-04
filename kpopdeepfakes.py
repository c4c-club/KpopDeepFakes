# -*- coding: utf-8 -*-
# @Time : 2020/8/4 13:37
# @Author : C4C
# @File : kpopdeepfakes.py
# @Remark : sipder of kpopdeepfakes.net

import random
import requests as rq
from bs4 import BeautifulSoup as bs


def get_idols_page_item(header,idol_url,min_page,max_page):
    video_item_list = []

    for index in range(min_page,max_page+1):
        print('正在获取第 ' + str(index) + ' 页')
        page_url = idol_url+'page/'+str(index)+'/'

        respones = rq.get(url=page_url, headers=header, timeout=60)
        #print(respones.status_code)
        if respones.status_code == 200:
            respones.encoding = 'utf=8'
            page_html = respones.text
            soup = bs(page_html, 'lxml')  # 返回网页
            video_list_container = soup.select_one('.kd-video-list-container')
            video_link = video_list_container.select('.video-link-container')
            for v in video_link:
                video_item_list.append(v.get('href'))
        else:
            print('网络连接错误')

        print('总共获取 '+str(len(video_item_list))+' 条')

    return video_item_list


def get_video_title_and_downloadlink(header,video_item_list,mode):
    downloadlink = []
    video_title = []
    str1 = ''
    str2 = ''

    for i in range(len(video_item_list)):
        url = video_item_list[i]
        print('正在获取 '+url)
        print('进度 '+str(i+1)+'/'+str(len(video_item_list)))

        respones = rq.get(url=url,headers=header,timeout=60)
        if respones.status_code == 200:
            respones.encoding = 'utf-8'
            page_html = respones.text
            soup = bs(page_html, 'lxml')  # 返回网页
            # title
            title = soup.select_one('.video-title').text
            if title is not None:
                video_title.append(title)
            else:
                video_title.append('找不到标题')

            #downloadlink
            video = soup.select_one('.video-js')
            video_download_link = video.select('source')[0].get('src')
            if video_download_link is not None:
                downloadlink.append(video_download_link)
            else:
                downloadlink.append('找不到链接')

        else:
            print('网络连接错误')

    file1 = open('directory.txt',mode,encoding='utf-8')
    for i in range(len(video_title)):
        str1 += video_title[i]+'\n'+downloadlink[i]+'\n'
    file1.write(str1+'\n以下为追加\n')
    file1.close()

    file2 = open('downloadlink.txt',mode,encoding='utf-8')
    for i in range(len(downloadlink)):
        str2 += downloadlink[i]+'\n'
    file2.write(str2 + '\n以下为追加\n')
    file2.close()




if __name__ == '__main__':
    # 定义随机header
    header1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Cookie': '_ga=;_gid=;kd_session_b='#此处添加自己浏览器的cookie
    }
    header2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Cookie': '_ga=;_gid=;kd_session_b='#此处添加自己浏览器的cookie
    }
    headList = [header1, header2]
    headerindex = random.randrange(0, len(headList))
    header = headList[headerindex]

    print('kpopdeepfakes.net下载器_V1.0_Create by c4c')
    idol_url = input("请输入idol页面的链接：")
    min_page = int(input("请输入开始下载页面序号："))
    max_page = int(input("请输入结束下载页面序号："))
    mode = input("请选择输入模式(a为追加模式，w为覆写模式)：")

    video_item_list = get_idols_page_item(header,idol_url,min_page,max_page)
    get_video_title_and_downloadlink(header, video_item_list,mode)

    input('任务完成，按任意键退出...')