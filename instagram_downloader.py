from selenium import webdriver
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC

# scroll everething
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


class instagramCrawler():
    def __init__(self, username, path):
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.instagram.com/' + username)
        self.posts = []

    def scroll(self, tempo=5):
        inicio = time.time()
        print('scroll the page and wait ', tempo)
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        while self.driver.find_elements(By.TAG_NAME, 'div'):
            if time.time() - inicio > tempo:
                break

    def get_posts(self):
        print('get the posts')
        raw = self.driver.find_elements(By.CLASS_NAME, "_2di5p")
        for post in raw:
            print('get the src of images')
            self.posts.append(post.get_attribute('src'))

    def download_post(self):
        print('clean duplicate ones')
        self.posts = list(set(self.posts))
        for post in self.posts:
            print('baixando' + post)
            pic_raw = requests.get(post)
            f = open('download/' + str(time.time()), 'wb')
            f.write(pic_raw.content)
            f.close()
        self.posts = []

    def run(self):
        self.get_posts()
        self.scroll()
        self.scroll()
        self.get_posts()
        self.scroll()
        self.scroll()
        self.get_posts()
        self.scroll()
        self.scroll()
        self.download_post()


username = input('Digite o nome de usuario:')
teste = instagramCrawler(username, 'download')
teste.run()
