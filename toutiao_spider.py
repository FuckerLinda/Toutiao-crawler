from bs4 import BeautifulSoup
import requests
import anti_spider
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import csv

#历史数据池
history=[]

"""
爬取头条热榜/热文周榜
参数select=1:爬取头条热榜
参数select=2:爬取热文周榜
"""
def hot(select):
    urls=["https://tophub.today/n/x9ozB4KoXb","https://tophub.today/n/20MdKa2ow1"]
    url = urls[int(select)-1]

    #反爬虫
    response=anti_spider.run(url)
    soup = BeautifulSoup(response.text, "lxml")

    #数据清洗：整理热榜
    data = soup.select(
        '#page > div.c-d.c-d-e > div.Zd-p-Sc > div:nth-child(1) > div.cc-dc-c > div > div.jc-c > table > tbody > tr'
    )
    results=[]
    for item in data:
        #逐条写入数组
        result = {
            'rank': item.select('tr > td')[0].get_text(),
            'count': item.select('tr > td')[2].get_text(),
            'title': item.select('tr > td.al > a')[0].get_text(),
        }
        print(result)
        increment_save(result,results,history)
    #将爬取数据存储至本地
    #头条热榜-爬虫数据存储
    if (int(select)-1)==0:
        if_save = input("是否存储？[y/n(default)]：")
        if if_save == 'y':
            name = input("输入文件名：(default:头条热榜.csv)")
            if name == "":
                name = '头条热榜.csv'
            with open(name, 'a+') as csvfile:
                fieldnames = ['rank', 'count', 'title']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
    #热文周榜-爬虫数据存储
    if (int(select) - 1) == 1:
        if_save = input("是否存储？[y/n(default)]：")
        if if_save == 'y':
            name = input("输入文件名：(default:热文周榜.csv)")
            if name == "":
                name = '热文周榜.csv'
            with open(name, 'a+') as csvfile:
                fieldnames = ['rank', 'count', 'title']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
    return results


"""
主动搜索
参数：
    content:搜索关键字
    pages:搜索页数
    search_type:搜索类型
"""
def search(keywords, pages, search_type):
    driver = webdriver.Chrome()
    #根据搜索类型选择url中参数pd的后缀，这个后缀决定了头条引擎的搜索类型
    #综合
    if search_type==1:
        suffix='synthesis'
    #资讯
    if search_type==2:
        suffix='information'
    #图片
    if search_type==3:
        suffix='atlas'
    #目标url
    url="https://so.toutiao.com/search?dvpf=pc&source=input&keyword=" + keywords + "&pd=" + suffix
    driver.get(url)
    time.sleep(2)
    # 获取每页标题并存储于results数组
    results=[]
    #选择爬取类型
    if search_type == 3:
        #爬取图片（可选择下载）
        atlas(driver, results)
    else:
        for page in range(1,pages+1):
            time.sleep(1)
            #爬取综合数据
            if search_type==1:
                synthesis(driver, results, page)
            #爬取资讯数据
            elif search_type==2:
                information(driver,results,page)
            # 前往下一页
            driver.find_element(By.XPATH,
                                "//a[@class='cs-view cs-view-inline-block cs-button cs-button"
                                "-l cs-button-default cs-button-square text-darker text-m rad"
                                "ius-m text-center text-nowrap margin-right-6'][" + str(page)
                                + "]/div[@class='cs-button-wrap']").click()
            time.sleep(1)
    #综合-爬虫数据存储
    if search_type==1:
        if_save = input("是否存储？[y/n(default)]：")
        if if_save == 'y':
            name = input("输入文件名：(default:synthesis.csv)")
            if name == "":
                name = 'synthesis.csv'
            with open(name, 'a+') as csvfile:
                fieldnames = ['page', 'title']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
    #资讯-爬虫数据存储
    if search_type==2:
        if_save = input("是否存储？[y/n(default)]：")
        if if_save == 'y':
            name = input("输入文件名：(default:information.csv)")
            if name == "":
                name = 'information.csv'
            with open(name, 'a+') as csvfile:
                fieldnames = ['page', 'title','content']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
    return results

"""
三种搜索结果都以集合的形式存储，这样可以避免内容重复。
"""

"""
综合搜索
"""
def synthesis(driver, results, page):
    # 获取标题
    titles = driver.find_elements(By.XPATH,
                                  "//div[@class='cs-view pad-bottom-3 cs-view-block "
                                  "cs-text align-items-center cs-header']/div[@class="
                                  "'flex-1 text-darker text-xl text-medium d-flex "
                                  "align-items-center overflow-hidden']/a[@class="
                                  "'text-ellipsis text-underline-hover']")
    # 存储当前页标题
    for title in titles:
        try:
            item = {'page': page, 'title': title.text}
            print(item)
        except Exception as e:
            continue
        increment_save(item, results, history)


"""
资讯搜索
"""
def information(driver,results,page):
    # 获取标题
    titles = driver.find_elements(By.XPATH,
                                  "//div[@class='cs-view pad-bottom-3 cs-view-block "
                                  "cs-text align-items-center cs-header']/div[@class="
                                  "'flex-1 text-darker text-xl text-medium d-flex "
                                  "align-items-center overflow-hidden']/a[@class="
                                  "'text-ellipsis text-underline-hover']")
    # 获取内容
    contents = driver.find_elements(By.XPATH,
                                  "//div[@class='cs-view cs-view-block cs-text "
                                  "align-items-center']/div[@class='flex-1 text-default"
                                  " text-m text-regular']/span[@class='text-underline-hover']")
    # 存储当前页标题及内容
    for i in range(len(titles)):
        try:
            item = {'page': page, 'title': titles[i].text, 'content':contents[i].text}
            print(item)
        except Exception as e:
            continue
        increment_save(item, results, history)


"""
图片搜索
"""
def atlas(driver,results):
    # 获取图片标题
    # 标题在属性中。因此想到由定位反获取属性
    raw_titles = driver.find_elements(By.XPATH,
                                  "//div[@class='cs-view margin-bottom-1 "
                                  "cs-view-block cs-text align-items-center text_2NW5ID']")
    titles=[]
    for title in raw_titles:
        titles.append(title.get_attribute("title"))
    # 图片src在属性中。因此想到由定位反获取属性
    raw_srcs = driver.find_elements(By.XPATH,"//img[@class='object-cover']")
    srcs=[]
    for src in raw_srcs:
        srcs.append(src.get_attribute("src"))

    picPath=input("请输入要存入的文件夹：")
    if picPath=="":
        picPath="测试文件夹"
    if not os.path.isdir(picPath):
        os.mkdir(picPath)
        #停顿，以防文件夹未被创建时就开始下载
        time.sleep(2)
    try:
        for i in range(len(srcs)):
            #请求图片并下载。超时则中断并抛出异常
            pic = requests.get(srcs[i], timeout=50)
            # 图片下载自带增量爬取
            dir = picPath + '/' + titles[i] + '.png'
            fp = open(dir, 'wb')
            fp.write(pic.content)
            fp.close()
    except Exception as e:
        print("图片下载时出现异常！")
        print(e)

    # 存储当前页标题及内容
    for i in range(len(titles)):
        item = {'title': titles[i], 'src': srcs[i]}
        print(item)
        increment_save(item, results, history)


"""
增量式爬取。历史记录表为history
参数：
    text:数据项
    array:临时数组
    history:历史数据池
若历史数据池中无数据项，则将数据项存入临时数组
"""
def increment_save(text,array,history):
    if text not in history:
        array.append(text)
        history.append(text)



"""
下方代码供测试用
"""
if __name__=="__main__":
    # 打印榜单
    select=input("请选择:\n1.头条热榜[default]\n2.热文周榜\n3.搜索\n输入：")
    if select=='2':
        hot('2')
    elif select=='3':
        search_type = input("请选择搜索类型:\n1.综合搜索[default]\n2.资讯\n3.图片\n输入：")
        keywords=input("请输入搜索内容：")
        if search_type not in ['1','2','3']:
            search_type=1
        pages=1
        if search_type in ['1','2']:
            pages=input("请选择页数[default=1]:")
            if pages=="":
                pages=1
            pages=int(pages)
        search_type = int(search_type)
        search(keywords, pages, search_type)
    else:
        hot('1')


