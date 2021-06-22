from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import csv
import re
import time

start = time.time()
#Creating CSV File
file = open('FinanceData.csv','w', newline='')
writer = csv.writer(file)

#Selenium Stuff
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\Firefox.exe')
myprofile = webdriver.FirefoxProfile(r'C:\Users\matth\AppData\Roaming\Mozilla\Firefox\Profiles\bv07xy71.default-1617838338767')

#header row
writer.writerow(['Ticker','Mkt Cap Now','MktCap Last Yr','Rev Now (B/M)','Rev Now','Rev last Yr','20DayMA','50DayMA','RSI','Margin'])

form_data = {'username': 'accounting@lowethluxuryproperties.com', 'pass': 'secretpassword'}

opts = Options()
opts.headless = True
driver = webdriver.Firefox(firefox_profile=myprofile,options=opts, firefox_binary=binary)
#['MDB','GRWG','GNRC','PII','AAPL','QCOM','ASML','INTC','ENPH','SEDG','ASX','CLF',
#        'RIO','STLD','MT','HZO','FB','PLTR','ETSY','PYPL','SQ','VEEV','CVX','PDD','BIDU',
#        'MO','TDOC','POOL','FCX','LPX','CP','NVCR','V','AMGN','CDE','COIN','NVDA',
#        'NFLX','MSFT','CF','DQ','DE','F','LUV','BA','TGT','WMT','LEN','PHM','DKNG','TLRY','DHI','XOM']

#list = ['MDB','GRWG','GNRC','PII','AAPL','QCOM','ASML','INTC','ENPH','SEDG','ASX','CLF',
#        'RIO','STLD','MT','HZO','FB','PLTR','ETSY','PYPL','SQ','VEEV','CVX','PDD','BIDU']
#list = ['MO','TDOC','POOL','FCX','LPX','CP','NVCR','V','AMGN','CDE','COIN','NVDA']
list = ['NFLX','MSFT','CF','DQ','DE','F','LUV','BA','TGT','WMT','LEN','PHM','DKNG','TLRY','DHI','XOM']

for ticker in list:
    time.sleep(10)
    url = 'https://finance.yahoo.com/quote/%s/key-statistics?p=%s' % (ticker, ticker)
    print(ticker)
    driver.get(url)

    #Marketcaps
    print(' Market Cap 1')
    try:
        mktcap1 = (driver.find_elements_by_css_selector("#Col1-0-KeyStatistics-Proxy > section > div > div > div > div > div > div > table > tbody > tr > td:nth-child(2)")[0].text);
    except:
        print("error")
        mktcap1 = "Error"
    mktcap1 = re.sub("[BT]","", mktcap1)
    print(' Market Cap 2')
    try:
        mktcap2 = (driver.find_elements_by_css_selector("#Col1-0-KeyStatistics-Proxy > section > div > div > div > div > div > div > table > tbody > tr > td:nth-child(4)")[0].text);
    except:
        print("error")
        mktcap2 = "NA"
    mktcap2 = re.sub("[BT]","", mktcap2)
    
    #Revenues
    url = 'https://ycharts.com/companies/%s/revenues' % (ticker)
    #time.sleep(5)
    driver.get(url)
    print(' Revenue 1')
    try:
        rev1 = (driver.find_elements_by_css_selector("#dataTableBox > div:nth-child(3) > div.dataColLeft > div > table > tbody > tr:nth-child(2) > td.col2")[0].text);
    except:
        print("error")
        rev1 = "Error"
    revnow = rev1
    
    if 'M' in rev1:
        rev1 = re.sub("[MBT]","", rev1)
        rev1 = float(rev1) / 1000
    #elif 'T' in rev1:
    #    rev1 = re.sub("[MBT]","", rev1)
    #    rev1 = int(float(rev1)) * 1000
    else:
        rev1 = re.sub("[MBT]","", rev1)
        
    print(' Revenue 2')
    try:
        rev2 = (driver.find_elements_by_css_selector("#dataTableBox > div:nth-child(3) > div.dataColLeft > div > table > tbody > tr:nth-child(6) > td.col2")[0].text);
    except:
        print("error")
        rev2 = "NA"

    if 'M' in rev2:
        rev2 = re.sub("[MBT]","", rev2)
        rev2 = float(rev2) / 1000
    #elif 'T' in rev1:
    #    rev2 = re.sub("[MBT]","", rev1)
    #    rev2 = float(rev1) * 1000
    else:
        rev2 = re.sub("[MBT]","", rev2)

    #ibd
    #url = 'https://www.zacks.com/stock/quote/%s?q=%s' % (ticker, ticker)
    #driver.get(url)
    #score = (driver.find_elements_by_css_selector("#premium_research > div > dl:nth-child(3) > dd > a > span")[0].text);
    #score = re.sub("[Top Btm%]","", score)

    #20DayMoving
    url = 'https://www.barchart.com/stocks/quotes/%s/technical-analysis' % (ticker)
    driver.get(url)
    print(' 20 Day MA')
    try:
        ma20d = (driver.find_elements_by_css_selector("#main-content-column > div > div > div > div:nth-child(1) > div > div > ng-transclude > table > tbody > tr:nth-child(2) > td:nth-child(2)")[0].text);
    except:
        print("error")
        ma20d = "NA"
    #50 Day
    print(' 50 Day')
    try:
        ma50d = (driver.find_elements_by_css_selector("#main-content-column > div > div > div > div:nth-child(1) > div > div > ng-transclude > table > tbody > tr:nth-child(3) > td:nth-child(2)")[0].text);
        print("it work")
    except:
        print("error")
        ma50d = "NA"
        
    #RSI
    print(" RSI")
    try:
        rsi = (driver.find_elements_by_css_selector("#main-content-column > div > div > div > div:nth-child(3) > div > div > ng-transclude > table > tbody > tr:nth-child(2) > td:nth-child(2)")[0].text);
    except:
        print("error")
        rsi = "NA"

    #Margin
    url = 'https://ycharts.com/companies/%s/gross_profit_margin' % (ticker)
    driver.get(url)
    print(" Margin")
    try:
        margin = (driver.find_elements_by_css_selector("#dataTableBox > div:nth-child(3) > div.dataColLeft > div > table > tbody > tr:nth-child(2) > td.col2")[0].text);
    except:
        print("error")
        margin = "NA"
    #Attribute = re.sub("[Things to remove]","", Attribute)

    #Template
    #url = '' % (ticker, ticker)
    #driver.get(url)
    #Attribute = (driver.find_elements_by_css_selector("")[0].text);
    #Attribute = re.sub("[Things to remove]","", Attribute)
    
    try:
        writer.writerow([ticker, mktcap1, mktcap2, revnow, rev1, rev2, ma20d, ma50d, rsi, margin])
    except:
        print("WRITE ROW NO WORKIE")
        writer.writerow([""])
file.close()
driver.close()
end = time.time()
print(end-start)
