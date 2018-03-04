"""Tentativa de criar um bot que baixa todas as fotos de um perfil."""
from selenium import webdriver
import requests
import time
import os
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
        try:
            self.driver.get('https://www.instagram.com/' + username)
        except Exception as e:
            print('erro ao abrir link')
            self.error_details(e)
        self.path = path
        self.check_path()
        self.posts = []
        self.scroll_size = str(
            self.driver.execute_script("return document.body.scrollHeight;"))

    def check_path(self):
        """Cuida do caminho de download."""
        if not os.path.exists(self.path):
            try:
                print('Criando path')
                os.makedirs(name=self.path, exist_ok=True)

            except Exception as e:
                self.error_details(e)
                return False
        else:
            print('path ok')
        return True

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
        raw = self.driver.find_elements(By.CLASS_NAME, "_2di5p")
        if raw:
            print('pegando o src das imagens')
            for post in raw:
                self.posts.append(post.get_attribute('src'))
        else:
            print('Nenhum Post encontrado, Verifique se o perfil é publico')

    def download_post(self):
        """Limpa os links duplicados e baixa as fotos."""
        print('clean duplicate ones')
        self.posts = list(set(self.posts))
        i = 0
        if self.posts:
            for post in self.posts:
                print('baixando' + post)
                pic_raw = requests.get(post)
                f = open(self.path + '/' + str(i), 'wb')
                f.write(pic_raw.content)
                i += 1
                f.close()
            self.posts = []

    def run(self):
        """Roda o crawler."""
        # baixar toda a pagina
        if self.path:
            footer = self.driver.find_element(By.TAG_NAME, 'footer')

            while True:
                antes = footer.location['y']
                self.scroll_page(direction='Down', tempo=2)
                depois = footer.location['y']
                self.get_posts()
                if antes == depois:
                    break

            self.download_post()
        else:
            pass


def main():
    """Essa é a main do projeto."""
    username = input('Digite o nome de usuario a ser procurado:')
    path = input('Digite a pasta de destino:')
    teste = instagramCrawler(username, path)
    teste.run()


if __name__ == '__main__':
    main()
