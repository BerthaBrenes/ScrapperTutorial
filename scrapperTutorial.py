from selenium import webdriver
import pandas as pd 
import selenium
import time 

driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver-v0.24.0-linux64/geckodriver')
driver.get('https://percentil.fr/vetement?sortMode=1&tipoPrenda=5&idRowsPerPage=1')
time.sleep(7)
papers = pd.DataFrame(columns = ['Articule','Likes','Price','Link',]) 

def scrapper(a):
    s = '/html/body/div[14]/div/main/section/div[3]/section/div/div/div[7]/div[2]/section/div[1]/div[{}]/div/div/li/div/article[1]/a/div/div[1]/img'.format(a+1)
    shoes = driver.find_element_by_xpath(s)
    print("Articule:",shoes.get_attribute('alt'))
    ln = '/html/body/div[14]/div/main/section/div[3]/section/div/div/div[7]/div[2]/section/div[1]/div[{}]/div/div/li/div/article[1]/a'.format(a+1)
    link = driver.find_element_by_xpath(ln)  
    print("link:",link.get_attribute('href'))
    li = '/html/body/div[14]/div/main/section/div[3]/section/div/div/div[7]/div[2]/section/div[1]/div[{}]/div/div/li/div/article[1]/div/span'.format(a+1)
    likes = driver.find_element_by_xpath(li)
    print("likes:",likes.text)
    pr = '/html/body/div[14]/div/main/section/div[3]/section/div/div/div[7]/div[2]/section/div[1]/div[{}]/div/div/li/div/article[2]/span[3]'.format(a+1)
    priceN = driver.find_element_by_xpath(pr)
    print("price:",priceN.text)
    try:
        pr = '/html/body/div[14]/div/main/section/div[3]/section/div/div/div[7]/div[2]/section/div[1]/div[{}]/div/div/li/div/article[2]/span[2]'.format(a+1)
        priceNe = driver.find_element_by_xpath(pr)
        print("price old:",priceNe.text)
        pf = '/html/body/div[14]/div/main/section/div[3]/section/div/div/div[7]/div[2]/section/div[1]/div[{}]/div/div/li/div/article[2]/span[3]'.format(a+1)
        priceN = driver.find_element_by_xpath(pf)
        print("Offer price",priceN.text)
    except selenium.common.exceptions.NoSuchElementException:
        pass
    papers.loc[len(papers)] = [shoes.get_attribute('alt'),likes.text,priceN.text, link.get_attribute('href')]

sub_button = driver.find_element_by_xpath('/html/body/div[12]/div/div/div[1]/button')
sub_button.click()        
cookies_button = driver.find_element_by_xpath('/html/body/div[5]/section/div/div[2]/div')
cookies_button.click()



for j in range(5):
    for i in range(4):
        scrapper(i)
    next_button = driver.find_element_by_xpath('/html/body/div[14]/div/main/section/div[3]/section/div/div/div[7]/div[3]/section/section/input[3]')
    next_button.click()

sort_by = papers.sort_values('Price')
sort=True
print(sort_by)
export_csv = papers.to_csv (r'/home/ordipret2/BerthaFiles/scraper/Articules.csv', index = None, header=True) 