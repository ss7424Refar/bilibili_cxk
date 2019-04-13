#!/usr/bin/python
#coding:utf-8
from requests import request
from bs4 import BeautifulSoup
import os
import sys
import time
from you_get import common as you_get

# 要查询到的页码
search_page = 1

# 当前查询的页码
page_number = 1

# 获得查询的关键字
search_keyword = sys.argv[1]

# 生成download.list文件
path = '../output/download.list'
if os.path.exists(path):
    os.remove(path)
else:
    os.mknod(path)

try:
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }
    response = request('GET', 'https://search.bilibili.com/all?keyword=' + search_keyword, headers=header)
    result = response.text

    print('==============================')
    # 创建一个BeautifulSoup解析对象
    soup = BeautifulSoup(result, "html.parser")

    # 查找总共多少页的标签
    lastPage_li = soup.find('li', class_='page-item last')
    lastPage_button = lastPage_li.find('button', class_='pagination-btn')
    total_page = int(lastPage_button.getText())
    print('查询出来的页码总共为：' + str(total_page) + '页')
    print('==============================')
except:
    print('获取总页数失败')
else:
    if total_page > 0:
        # 拿到命令行的第二个参数 页数
        if len(sys.argv) > 1:
            search_page = int(sys.argv[2])
            if total_page < search_page:
                search_page = total_page
        # 如果没有指定，就为总的页数
        else:
            search_page = total_page

        # 开始循环请求
        while page_number <= search_page:
            url = 'https://search.bilibili.com/all?keyword=' + search_keyword + '&page=' + str(page_number)
            time.sleep(2)
            response = request('GET', url, headers=header)
            result = response.text
            # 创建一个BeautifulSoup解析对象
            soup = BeautifulSoup(result, "html.parser")
            # 找到有avid的span标签
            head_lines = soup.find_all('span', class_='type avid')
            file = open(path, 'w')
            file.write('\n')
            file.write('######### 第' + str(page_number) + '页 ############\n')
            for head_line in head_lines:
                av_id = head_line.get_text()
                file.write(av_id + '\n')
                try:
                    # 开始下载
                    download_url = 'https://www.bilibili.com/video/' + av_id
                    # sys传递参数执行下载，就像在命令行一样
                    sys.argv = ['you-get', '-o', '../output/', download_url]
                    you_get.main()
                except:
                    file.write(av_id + '=============> 下载失败\n')
            page_number += 1






