from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    url = 'https://www2.bot.com.tw/house/'
    try:
        options = webdriver.FirefoxOptions()
        options.add_argument('--private')  # 無痕模式
        options.add_argument('--headless')
        # executable_path 輸入 web driver 執行檔的位置，下載網址
        # https://github.com/mozilla/geckodriver/releases
        driver = webdriver.Firefox(
            options=options,
            executable_path='geckodriver.exe',
			service_log_path='nul')	#不要產生 geckodriver.log
        # 等待網頁載入完畢，最多等60秒
        driver.set_page_load_timeout(60)
        driver.get(url)

        # 定位日期輸入欄位, 並輸入日期
        element = driver.find_element_by_id('fromdate_TextBox')
        element.send_keys('1090101')
        element = driver.find_element_by_id('todate_TextBox')
        element.send_keys('1100101')

        # 定位選單所在欄位並點擊
        element = driver.find_element_by_id('purpose_DDL')
        element.click()
        # 巡覽選單, 點擊對應選項
        for option in element.find_elements_by_tag_name('option'):
            if option.text == '住宅':
                option.click()

        # 定位選單所在欄位並點擊
        element = driver.find_element_by_id('PageCount_DDL')
        element.click()
        # 巡覽選單, 點擊對應選項
        for option in element.find_elements_by_tag_name('option'):
            if option.text == '50':
                option.click()

        # 點擊送出按鈕
        element = driver.find_element_by_id('Submit_Button').click()

        # 等待目標表格出現，等待最多5秒
        element = WebDriverWait(
            driver, 5).until(
            expected_conditions.presence_of_element_located(
                (By.ID, 'House_GridView')))

        # page_source 可以回傳目前瀏覽器所看到的網頁文件
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        table = soup.find(id='House_GridView')
        for row in table.find_all('tr'):
            print([s for s in row.stripped_strings])
    finally:
        driver.quit()  # 關閉瀏覽器, 結束 webdriver process
