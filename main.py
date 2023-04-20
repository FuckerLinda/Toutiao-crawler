from datetime import datetime
from toutiao_spider import *

#记录程序开始时间
date=datetime.now()
print("爬虫于",end="")
print(date.strftime("%Y-%m-%d, %H:%M:%S"),end="")
print("启动")

start_time=date.timestamp()
while(True):
    print("============================================")
    #爬取渠道选择
    select = input("请选择:\n1.头条热榜\n2.热文周榜\n3.搜索\n4.退出[default]\n输入：")
    if select == '1':
        hot('1')
    elif select == '2':
        hot('2')
    elif select == '3':
        #搜索类型选择
        search_type = input("请选择搜索类型:\n1.综合搜索\n2.资讯\n3.图片\n4.返回\n5.退出[default]\n输入：")
        keywords = input("请输入搜索内容：")
        if search_type=='4':
            continue
        elif search_type not in ['1', '2', '3']:
            break
        pages = 1
        #爬取页数选择
        if search_type in ['1','2']:
            pages = input("请选择页数[default=1]:")
        try:
            pages = int(pages)
        except:
            pages = 1
        search_type = int(search_type)
        search(keywords, pages, search_type)
    else:
        break
    print("============================================")

end_time=datetime.now().timestamp()
#记录程序结束时间
elapsed_time=end_time-start_time
print("程序运行时长：{:.2f}秒".format(elapsed_time))