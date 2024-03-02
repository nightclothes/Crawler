#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2023/11/30 16:32
# @Author  : 雷智杰

import random
import time
import requests
from lxml import etree
from colorama import Fore


def log(status: bool, message: str):
    if status:
        print(Fore.GREEN + "[+]{}".format(message))
    else:
        print(Fore.RED + "[-]{}".format(message))
    print(Fore.RESET + '', end='')


def get_response(url: str):
    # 获取请求
    url = url
    # 硬件伪装 访问地址伪装 伪装用户真实信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'referer': url,
        'cookie': 'bid=9boYgqRNcPg; _pk_id.100001.4cf6=bce09e5564298f11.1701418413.; '
                  '__utmz=30149280.1701419988.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '
                  '__utmz=223695111.1701419988.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="108309"; '
                  '_vwo_uuid_v2=DE6F2BA4B58FCFBECF3F26C11607C10E2|ae33e44237c82f55774eae32c8d5793f; '
                  '_pk_ses.100001.4cf6=1; __utma=30149280.1466019034.1701419988.1701447595.1701496344.3; '
                  '__utmc=30149280; __utma=223695111.8753585.1701419988.1701447595.1701496344.3; '
                  '__utmb=223695111.0.10.1701496344; __utmc=223695111; dbcl2="276239365:ZO3TO4r93Jk"; ck=P93t; '
                  'push_noty_num=0; push_doumail_num=0; __utmv=30149280.27623; __utmb=30149280.10.10.1701496344; '
                  'frodotk_db="5127fe97f9f1ef79f377fbc7edd5ce6b"; ap_v=0,6.0'}
    response = requests.get(url, headers=headers)
    # 返回response
    if response.status_code == 200:
        return response
    else:
        return None


def save_info(path: str, comments: list):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(comments))
    log(True, "保存成功")


def get_info(comments_max_page):
    num = 1
    # 解析电影
    for i in range(10):
        # 解析目录
        directory_url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        directory_response = get_response(directory_url)
        if directory_response is None:
            log(False, "获取第{}页目录信息失败".format(i + 1))
            continue
        log(True, "开始获取第{}页目录信息".format(i + 1))
        directory_html = directory_response.text
        directory_web = etree.HTML(directory_html)
        # 解析电影
        for j in directory_web.xpath('//*[@id="content"]/div/div[1]/ol/li'):
            movie_url = j.xpath('./div/div[2]/div[1]/a/@href')[0]
            movie_response = get_response(movie_url)
            if movie_response is None:
                log(False, "获取第{}个电影信息失败".format(num))
                num = num + 1
                continue
            log(True, "开始获取第{}个电影信息".format(num))
            num = num + 1
            movie_html = movie_response.text
            movie_web = etree.HTML(movie_html)
            # 电影名
            title = j.xpath('.//span[@class="title"]/text()')[0]
            # 导演
            director = movie_web.xpath('//*[@id="info"]//a[@rel="v:directedBy"]/text()')[0]
            # 上映日期
            date = movie_web.xpath('//*[@id="info"]//span[@property="v:initialReleaseDate"]/text()')[0]
            # 替换掉 / 否则保存文件时会出错FileNotFoundError
            date = date.replace('/', ' ')
            # 解析短评
            comments = []
            for page in range(comments_max_page):
                # 伪装访问速率
                time.sleep(random.uniform(1, 2))
                # 短评URL
                comment_url = movie_url + 'comments?start={}&limit=20&status=P&sort=new_score'.format(page * 20)
                # 解析评论
                comment_response = get_response(comment_url)
                if comment_response is None:
                    log(False, "获取第{}页评论信息失败".format(page + 1))
                    continue
                log(True, "开始获取第{}页评论信息".format(page + 1))
                comment_html = comment_response.text
                comment_web = etree.HTML(comment_html)
                for comment in comment_web.xpath('//*[@id="comments"]//span[@class="short"]/text()'):
                    comments.append(comment.replace('\n', ''))
            save_info('./comments/{}.txt'.format(title + '+' + date + '+' + director), comments)


if __name__ == '__main__':
    get_info(30)
