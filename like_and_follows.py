from selenium import webdriver
import requests
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
name = 'superbot1300'
senha = 'passwordprojeto'


class intagramBot():
    """Classe pra baixar fotos de um perfil publico."""

    def __init__(self, hashtag, thresholdPosts):
        """Abre o browser no perfil e inicializa post."""
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.instagram.com/accounts/login/')
        self.wait(5)
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_locate(driver.find_element(By.NAME, 'username')))
        input_name = self.driver.find_element(By.NAME, 'username')
        input_senha = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.CSS_SELECTOR, '._qv64e')
        input_name.send_keys(name)
        input_senha.send_keys(senha)
        login_button.click()
        try:
            self.driver.get(
                'https://www.instagram.com/explore/tags/' + hashtag)
        except Exception as e:
            print('erro ao abrir link')
            self.error_details(e)
        self.posts = []
        self.scroll_size = str(
            self.driver.execute_script("return document.body.scrollHeight;"))

    @staticmethod
    def error_details(e):
        """Mostra ou oculta detalhes de errros."""
        op = input('Deseja ver os detalhes?(Y/n)')
        if (op == 'n') or (op == 'N'):
            print('detalhes:', e)
        else:
            pass

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

    @staticmethod
    def wait(tempo):
        """Espera um determinado tempo."""
        inicio = time.time()
        while True:
            if time.time() - inicio > tempo:
                return

    def get_posts(self):
        """Pega o link das foto disponiveis no dom."""
        print('get the posts')
        raw = self.driver.find_elements(By.CSS_SELECTOR,
                                        '._mck9w._gvoze._tn0ps a')
        if raw:
            print('pegando o link dos posts')
            for post in raw:
                self.posts.append(post.get_attribute('href'))
                print(self.posts.append(post.get_attribute('href')))
        else:
            print(
                'Nenhum Post encontrado, Verifique se é uma hashtag utilizada')

    def doLikesAndFollows(self):
        if (self.posts):
            for post in self.posts:
                try:
                    self.driver.get(post)
                except Exception as e:
                    print('erro ao abrir link')
                    self.error_details(e)
                print("dando like e seguindo")
                self.driver.find_element_by_css_selector(
                    '_qv64e._iokts._4tgw8._njrw0').click(
                )  # botao de seguir //isto é um buttom (tag buttun)
                self.driver.find_element_by_css_selector(
                    '_eszkz._l9yih').click(
                )  # botao de like //isto é um link (uma tag a)

    def run(self):
        footer = self.driver.find_element(By.TAG_NAME, 'footer')
        numberOfPosts = 0
        threshold = 100
        while True:
            numberOfPosts += 1
            antes = footer.location['y']
            self.scroll_page(direction='Down', tempo=1)
            depois = footer.location['y']
            self.get_posts()
            if ((antes == depois) or (numberOfPosts == threshold)):
                break

        self.doLikesAndFollows()


def main():
    """Essa é a main do projeto."""
    hashtag = input('adicione aqui a hashtag desejada:')
    thresholdPost = 100
    teste = intagramBot(hashtag, thresholdPost)
    teste.run()


if __name__ == '__main__':
    main()
