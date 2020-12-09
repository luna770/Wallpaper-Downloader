#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Project_name: 王者荣耀壁纸下载器
@Author: bilibili晨霜若雪
@Description: 可以下载单个/所有英雄的全部壁纸，分辨率可选且和官网（https://pvp.qq.com/web201605/wallpaper.shtml"）保持一致，支持增量下载
@Update_date: 2020-12-09
@Version: 2.2 优化皮肤命名，修复bug
"""

import os
from urllib.parse import unquote
import requests
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43 '
}
sizes = {
    '1': '215 x 120',
    '2': '1024 x 768',
    '3': '1280 x 720',
    '4': '1280 x 1024',
    '5': '1440 x 900',
    '6': '1920 x 1080',
    '7': '1920 x 1200',
    '8': '1920 x 1440',
}


def getAllHeroName():
    # 英雄信息名字相关url
    heroes_url = 'https://pvp.qq.com/web201605/js/herolist.json'
    response = requests.get(heroes_url, headers=headers)
    hero_data = response.json()
    hero_name = list(map(lambda x: x['cname'], hero_data))
    return hero_name


def selectSize():
    print("\n" + "-" * 25 + "【选择分辨率】" + "-" * 25)
    for item in sizes.items():
        print('\t', item[0], '\t\t', item[1])
    print("-" * 62)
    size_key = input("请输入数字指令：")

    if size_key.isdigit() and int(size_key) in list(range(1, 9)):
        return size_key
    else:
        print("请输入数字1-8")
        showMenu(2)


def spider(heroName, size_key, is_one_hero=False):
    url = 'http://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?sDataType=JSON&SearchKey' \
          '=sProdName&SearchValue=' + heroName + '&iTypeId=2&iActId=2735'
    response = requests.get(url, headers=headers)
    data = response.json()
    skin_count = int(data['iTotalLines'])
    for i in range(skin_count):
        img_url_raw = data['List'][i]['sProdImgNo_' + size_key].replace('F200', 'F0')
        img_url = unquote(img_url_raw, 'utf-8')
        img_name = (unquote(data['List'][i]['sProdName']) + '.jpg').strip()
        # 解决因接口造成的‘后羿-如梦令.jpg’下载出错问题
        if img_name == '后羿-如梦令.jpg':
            img_url = 'http://shp.qpic.cn/ishow/2735031110/1583893704_84828260_20058_sProdImgNo_' + size_key + '.jpg/0'
        download_img(img_url, sizes[size_key], img_name)
    if is_one_hero:
        showMenu(2)


def download_img(img_url, size_folder, img_name):
    # 建立目录
    save_dir = os.path.join("王者荣耀全英雄壁纸", size_folder)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 修复‘\d:’开头的文件名导致os.path.join()的异常问题，干脆删除
    if ':' in img_name:
        return
    save_path = os.path.join(save_dir, img_name)

    # 文件不存在时才写入（增量下载）
    if not os.path.exists(save_path):
        print(" --> ", end=" ")
        content = requests.get(img_url, headers=headers).content
        with open(save_path, 'wb') as f:
            f.write(content)
        print(img_name + " 下载完成")


# 显示主菜单（在函数controller中调用controller）
def showMenu(second):
    time.sleep(second)
    controller()


def controller():
    print('\n>>----------------- 【王者荣耀壁纸下载器-V2.2】 --------------------<<\n')
    print("\t1\t下载单个英雄壁纸\n\t2\t下载所有英雄壁纸\n\t3\t帮助")
    print('\n>>-------------------------------------------- @b站晨霜若雪 --<<')

    instruction = input("请输入数字指令：")
    heroNames = getAllHeroName()
    if instruction == '1':
        heroName = input("请输入英雄名字：")
        if heroName not in heroNames:
            print("英雄【" + heroName + "】不存在！")
            showMenu(2)
        size_key = selectSize()
        spider(heroName, size_key, True)
    elif instruction == '2':
        size_key = selectSize()
        # print("【共" + str(len(heroNames)) + "英雄】\n")
        print(" ===>开始下载全部壁纸===>")
        for heroName in heroNames:
            spider(heroName, size_key)
        print("全部壁纸下载完成! 程序在8秒后自动退出...")
        time.sleep(8)
    elif instruction == '3':
        print("\n" + "-" * 30 + "【帮助信息】" + "-" * 30 + "\n\n\t【作者】：哔哩哔哩@晨霜若雪\n\t【描述】：可以下载单个/所有英雄的"
              "全部壁纸，分辨率可选且和官网保持一致\n\t" + "【地址】：https://github.com/"
              "luna770/WallpaperDownloader，欢迎star！\n\n" + "-" * 70)
        showMenu(7)
    else:
        print("请输入正确的指令！")
        showMenu(2)


if __name__ == '__main__':
    controller()
