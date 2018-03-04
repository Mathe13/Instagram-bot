from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from instagram_downloader import instagramCrawler
user_name = 'teste'
senha = 'teste'

driver = webdriver.Firefox()
driver.get('https://www.instagram.com/accounts/login/')
instagramCrawler.wait(5)
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_locate(driver.find_element(By.NAME, 'username')))
input_name = driver.find_element(By.NAME, 'username')
input_senha = driver.find_element(By.NAME, 'password')
login_button = driver.find_element(By.CSS_SELECTOR, '._qv64e')
input_name.send_keys(user_name)
input_senha.send_keys(senha)
login_button.click()
