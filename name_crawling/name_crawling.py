from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip



def crawling_name():
    #브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options) 
    url = "https://koreanname.me/"
    driver.get(url)
    
    before_h = driver.execute_script("return document.body.scrolHeight")
    
    # "더보기" 버튼 10번 클릭까지 스크롤 내리기
    count = 0
    while True:
        if count == 10:
            break
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        new_h = driver.execute_script("return document.body.scrollHeight")
        
        button = driver.find_element(By.CSS_SELECTOR, '#__next > section > section > main > div > div > div:nth-child(3) > button')
        button.click()
        
        if new_h == before_h:
            break
        
        before_h = new_h
        count += 1
    
    # 이름 크롤링    
    name = []
    
    row1 = driver.find_element(By.XPATH, '//*[@id="__next"]/section/section/main/div/div/div[2]/div[5]/div[1]/div/div/div/div/div/div/table/tbody')
    values = row1.find_elements(By.TAG_NAME, 'a')
    
    for i in values:
        name.append(i.accessible_name)
        
    row2 = driver.find_element(By.XPATH, '//*[@id="__next"]/section/section/main/div/div/div[2]/div[5]/div[2]/div/div/div/div/div/div/table/tbody')
    values = row2.find_elements(By.TAG_NAME, 'a')
    
    for i in values:
        name.append(i.accessible_name)
    
    # 중복된 이름 제거    
    result = []
    for value in name:
        if value not in result:
            result.append(value)
    
    file_name = './name_list.txt'

    with open(file_name, 'w+') as file:
        file.write('\n'.join(result))

def crawling_lastname():
    #브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options) 
    url = "https://namu.wiki/w/%ED%95%9C%EA%B5%AD%EC%9D%98%20%EC%84%B1%EC%94%A8%EB%B3%84%20%EC%9D%B8%EA%B5%AC%20%EB%B6%84%ED%8F%AC"
    driver.get(url)
    
    last_names = []
    
    for i in range(2, 102):
        # row = driver.find_element(By.XPATH, '//*[@id="xeZKSV0Ou"]/div[2]/div/div/div[1]/div[7]/div/div/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[11]/div/div/div/div[1]/div/div[4]/div[1]/table/tbody/tr[{}]/td[2]/div/a[1]'.format(i))
        element = driver.find_element(By.XPATH, '//*[@id="xeZKSV0Ou"]/div[2]/div/div/div[1]/div[7]/div/div/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[11]/div/div/div/div[1]/div/div[4]/div[1]/table/tbody/tr[{}]/td[2]/div/a[1]'.format(i))
        last_name = element.accessible_name
        last_names.append(last_name)
        
    file_name = './lastname_list.txt'

    with open(file_name, 'w+') as file:
        file.write('\n'.join(last_names))

def crawling_chinese():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options) 
    url = "https://namu.wiki/w/%ED%95%9C%EC%9E%90/%EC%9D%B8%EB%AA%85%EC%9A%A9%20%ED%95%9C%EC%9E%90%ED%91%9C"
    driver.get(url)
    
    chinese = []
    
    table = driver.find_element(By.XPATH, '//*[@id="xeZKSV0Ou"]/div[2]/div/div/div[1]/div[7]/div/div/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[11]/div/div/div/div[1]/div/div[5]/div[2]/table/tbody')
    element = table.find_elements(By.CLASS_NAME, 's3zppxXT')
        
    for i in element:
        chinese.append(i.accessible_name)        
    
    result = []
    for value in chinese:
        if value not in result:
            result.append(value)
            if len(result) == 1000:
                break
    
    
    print("text")
    
    file_name = './chinese.txt'

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write('\n'.join(result))
    

def main():
    # crawling_name()
    # crawling_lastname()
    crawling_chinese()
    
    

if __name__ == "__main__":
    main()