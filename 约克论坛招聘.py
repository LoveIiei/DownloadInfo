from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import re
import random



#将网页滑动
def drop_down():
    for x in range(1, 10, 4):
        time.sleep(1)
        j = x / 9
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)
#网页地址
url = 'https://job.yorkbbs.ca'
i = 1
#打开网页，并自动下滑（不下滑有数量限制)，去拿到规定数量的所有网站链接
ser = Service('/Users/huawy/Documents/pythonscripts/chromedriver')
driver = webdriver.Chrome(service=ser)
driver.get(url)
time.sleep(1)
drop_down()

#拿到网址源码
mainsource = driver.page_source
fsoup = BeautifulSoup(mainsource, 'html.parser')
#print(mainsource)
#拿到所有链接
lists = fsoup.find('div', class_="post-list").find_all('a')
#提前准备好所有重要变量
links = []
titles = []
contacts = []
PhoneNumbers = []
desLists = []
shortInfos = []
actAddresses = []
types = []
#print(job_lists)
#尝试打开储存用的excel文件，并提取里面内容用做对比
try:
    xlsx_file = "Yorkbbstry.xlsx"
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active
    for column in sheet.iter_rows(2):
        titles.append(column[1].value)
        contacts.append(column[2].value)
        PhoneNumbers.append(column[3].value)
        desLists.append(column[4].value)
        shortInfos.append(column[5].value)
        actAddresses.append(column[6].value)
    print("现在已有的")
    print(titles)
    print(contacts)
    print(PhoneNumbers)
    print(desLists)
    print(shortInfos)
    print(actAddresses)
#如果还没有这个表格
except:
    print("你还没有创建这个表格")
#循环每个工作
for job in lists:
    l = 0
    w = 0
    try:
        #拿到每个工作自己的网址
        halflink = job.get('href')
        if halflink[1] == 'd':
            link = 'https://job.yorkbbs.ca' + halflink
            driver.get(link)
            time.sleep(2)
            driver.find_element(By.XPATH, '/html/body/div/div[1]/main/div[2]/aside/div[1]/div[2]/div[2]/button').click()
            source = driver.page_source
            time.sleep(2)
            soup = BeautifulSoup(source, 'html.parser')
            # print(soup)
            Info = soup.find('div', class_="editor-txt-content post-content").find_all('p')
            Info = str(Info)
            shortInfo = ''.join(Info)
            try:
                address = soup.find('a', class_="post-map google-map")
                location = address.get('href')
                actaddress = re.findall(r'query=(\d*\.\d*\,\-\d*\.\d*)', location)[0]
            except:
                actaddress = ""
            codeLanguege = re.findall(r'<(.*?)>', shortInfo)
            for p in codeLanguege:
                shortInfo = shortInfo.replace(p, '')
            nostrting = ['<p>', '</p>', '<br/>', ' ', ',', '<', '>']
            for i in nostrting:
                shortInfo = shortInfo.replace(i, '')
            shortInfo = shortInfo.strip('[]')
            shortInfo = shortInfo.strip('/')
            contact = soup.find('span', class_="member-item__value").text
            PhoneNumber = soup.find('span', class_="member-item__phone").text
            title = soup.find('div', class_="post-title").text
            deslist = []
            describe = soup.find_all('div', class_="cont")
            for des in describe:
                deslist.append(des.contents[0])
                # print(des.contents[0])
            type = describe[1]
            types.append(type)
            deslist = ' '.join(deslist)
            title = title.strip()
            noneed = ["置顶", "加急", "精华", ' ']
            for p in noneed:
                title = title.replace(p, '')
            #如果之前没有excel文件，直接添加信息到新文件
            if not titles:
                print("正在添加信息到新文件")
                print(title)
                print(contact)
                print(PhoneNumber)
                print(deslist)
                print(shortInfo)
                print(actaddress)
                titles.append(title)
                contacts.append(contact)
                PhoneNumbers.append(PhoneNumber)
                desLists.append(deslist)
                shortInfos.append(shortInfo)
                actAddresses.append(actaddress)
            else:
                #如果已有文件，检查标题和电话号码是否一样，只添加新信息
                if not title in titles or not PhoneNumber in PhoneNumbers:
                    print("正在添加信息到文件")
                    titles.append(title)
                    contacts.append(contact)
                    PhoneNumbers.append(PhoneNumber)
                    desLists.append(deslist)
                    shortInfos.append(shortInfo)
                    actAddresses.append(actaddress)
                else:
                    print("信息已存在")
                print(title)
                print(contact)
                print(PhoneNumber)
                print(deslist)
                print(shortInfo)
                print(actaddress)
        time.sleep(1)
    except:
        print("信息未找到")
driver.quit()
print(titles)
print(contacts)
print(PhoneNumbers)
print(desLists)
print(shortInfos)
print(actAddresses)
#将信息写入excel表格
df = pd.DataFrame(
        {
            "职位": titles,
            "联系人": contacts,
            "电话": PhoneNumbers,
            "职位简介": desLists,
            "职位介绍": shortInfos,
            "地址": actAddresses,
        }
    )
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('Yorkbbstry.xlsx')
# write dataframe to excel
df.to_excel(writer)
# Close the Pandas Excel writer and output the Excel file.
writer.save()
for ty in types:
    path = '~/rolepics/'
    num = 0
    try:
        if ty == "医护护理":
            num = random.randint(0, 5)
            print(path + "医护护理/" + str(num) + ".jpeg")
        elif ty == "司机搬运":
            num = random.randint(0, 5)
            print(path + "司机搬运/" + str(num) + ".jpeg")
        elif ty == "装修":
            num = random.randint(0, 5)
            print(path + "装修/" + str(num) + ".jpeg")
        elif ty == "财务审计":
            num = random.randint(0, 5)
            print(path + "财务审计/" + str(num) + ".jpeg")
        elif ty == "销售相关":
            num = random.randint(0, 5)
            print(path + "销售相关/" + str(num) + ".jpeg")
        elif ty == "餐饮相关":
            num = random.randint(0, 5)
            print(path + "餐饮相关/" + str(num) + ".jpeg")
        elif ty == "Others":
            num = random.randint(0, 5)
            print(path + "Others/" + str(num) + ".jpeg")
    except:
        num = random.randint(0, 5)
        print(path + "Others/" + str(num) + ".jpeg")
print("已结束")