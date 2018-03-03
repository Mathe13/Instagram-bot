from selenium import webdriver
import requests
import time
from selenium.webdriver.common.by import By

# from selenium.webdriver.support.ui import WebDriverWait as Wait

# from selenium.webdriver.support import expected_conditions as EC

# scroll everething
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


class instagramCrawler():
    """Classe pra baixar fotos de um perfil publico."""

    def __init__(self, username, path):
        """Abre o browser no perfil e inicializa post."""
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.instagram.com/' + username)
        self.posts = []
        self.scroll_size = str(
            self.driver.execute_script("return document.body.scrollHeight;"))

    def scroll_page(self, direction, tempo=3):
        """Dá um scroll na pagina."""
        print('scroll ' + direction + ' e espera ' + str(tempo))
        if direction == 'Down':
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight+" +
                self.scroll_size + ");")
        if direction == 'Up':
            self.driver.execute_script(
                "window.scrollTo(0, " + "document.body.scrollHeight-" +
                self.scroll_size + ");")
        self.wait(tempo)
        return self.driver.execute_script("return document.body.scrollTop;")

    def wait(self, tempo):
        """Espera um determinado tempo."""
        inicio = time.time()
        while True:
            if time.time() - inicio > tempo:
                return

    def get_posts(self):
        """Pega o link das foto disponiveis no dom."""
        print('get the posts')
        raw = self.driver.find_elements(By.CLASS_NAME, "_2di5p")
        for post in raw:
            print('get the src of images')
            self.posts.append(post.get_attribute('src'))

    def download_post(self):
        """Limpa os links duplicados e baixa as fotos."""
        print('clean duplicate ones')
        self.posts = list(set(self.posts))
        i = 0
        for post in self.posts:
            print('baixando' + post)
            pic_raw = requests.get(post)
            f = open('download/' + str(i), 'wb')
            f.write(pic_raw.content)
            i += 1
            f.close()
        self.posts = []

    def run(self):
        """Roda o crawler."""
        # baixar toda a pagina

        footer = self.driver.find_element(By.TAG_NAME, 'footer')

        while True:
            antes = footer.location['y']
            self.scroll_page(direction='Down', tempo=2)
            depois = footer.location['y']
            self.get_posts()
            if antes == depois:
                break

        self.download_post()


username = input('Digite o nome de usuario:')
teste = instagramCrawler(username, 'download')
teste.run()
