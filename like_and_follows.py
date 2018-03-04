from selenium import webdriver
import requests
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
name = 'superbot1300'
senha = 'passwordprojeto'


class intagramBot():
    """Classe pra baixar fotos de um perfil publico."""

    def __init__(self):
        self.driver = webdriver.Firefox()

        self.hashtags = []
        self.takeTopHashtags()

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

        while True:
            url_now = self.driver.current_url
            if url_now == 'https://www.instagram.com/':
                break
        """try:
            self.driver.get('https://www.instagram.com/explore/tags/' + hashtag)
        except Exception as e:
            print('erro ao abrir link')
            self.error_details(e)"""
        # self.logout() #teste do logout
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

    def takeTopHashtags(self):
        """Pega as # dispoiveis no dom"""
        self.driver.get('https://top-hashtags.com/instagram/')
        print('take top #')
        raw = self.driver.find_elements_by_css_selector(
            '.tht-tag.small-7.medium-9.columns>a')
        if raw:
            print('top #')
            for hashtag in raw:
                self.hashtags.append(hashtag.text)
                print(hashtag.text)
        else:
            print('Nenhuma # encontrada')

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
        """Pega o link dos post disponiveis no dom."""
        print('get the posts')
        raw = self.driver.find_elements_by_css_selector(
            '._mck9w._gvoze._tn0ps>a')
        if raw:
            print('pegando o link dos posts')
            for post in raw:
                self.posts.append(post.get_attribute('href'))
        else:
            print(
                'Nenhum Post encontrado, Verifique se é uma hashtag utilizada')

    def doLikesAndFollows(self):
        print('Exec doLikesAndFollows')
        if (self.posts):
            print('clean duplicate ones')
            self.posts = list(set(self.posts))
            for post in self.posts:

                try:
                    self.driver.get(post)
                except Exception as e:
                    print('erro ao abrir link')
                    self.error_details(e)

                try:
                    pageErr = self.driver.find_element_by_css_selector(
                        '.error-container.-cx-PRIVATE-ErrorPage__errorContainer'
                    )  # Se encontrar significa q houve um erro na pagina
                except:
                    pageErr = False
                if (pageErr):
                    self.posts = [
                        item for item in self.posts if (item != post)
                    ]
                else:
                    try:
                        followed = self.driver.find_element_by_css_selector(
                            '._qv64e._jqf0k._4tgw8._njrw0'
                        )  # Se encontrar significa q ja está followed
                    except:
                        followed = False

                    liked = self.verify_if_is_liked()

                    if (followed == False):
                        self.driver.find_element_by_css_selector(
                            '._qv64e._iokts._4tgw8._njrw0'
                        ).click(
                        )  # botao de seguir //isto é um buttom (tag buttun)
                        # self.wait(thresholdTimeFollow)

                    if (liked == False):
                        like_button = self.driver.find_element_by_css_selector(
                            '._eszkz._l9yih')
                        while True:
                            # print('espera')
                            if like_button.is_enabled():
                                # print('esperei')
                                break
                        like_button.click()
                        # botao de like //isto é um link (uma tag a)

                    if (liked and followed):
                        # print(len(self.posts))
                        self.posts = [
                            item for item in self.posts if (item != post)
                        ]
                        # print(len(self.posts))

                    while True:
                        if not self.verify_if_is_liked() == False:
                            break

    def logout(self):
        self.driver.get("https://www.instagram.com/" + name + "/")
        self.wait(5)
        self.driver.find_element_by_css_selector('._q8y0e').click()
        # botão q abre o modal de logout
        self.wait(2)
        botoes = self.driver.find_elements_by_css_selector('._o2wxh > button')
        botoes[3].click()

    def verify_if_is_liked(self):
        try:
            liked = self.driver.find_element_by_css_selector(
                '._eszkz._l9yih>span._8scx2.coreSpriteHeartFull'
            )  # se encontrar significa que ainda n foi curtido
        except:
            return False
        return True

    def get_folow_button(self):
        try:
            follow_button = self.driver.find_element_by_css_selector(
                '._qv64e._iokts._4tgw8._njrw0')
            return follow_button
        except NoSuchElementException:
            return False

    def run(self, thresholdPosts):
        # self.takeTopHashtags()
        for hashtag in self.hashtags:
            try:
                self.driver.get(
                    'https://www.instagram.com/explore/tags/' + hashtag[1:])
            except Exception as e:
                print('erro ao abrir link')
                self.error_details(e)

            footer = self.driver.find_element(By.TAG_NAME, 'footer')
            numberOfPosts = 0

            while True:
                numberOfPosts += 1
                antes = footer.location['y']
                self.scroll_page(direction='Down', tempo=1)
                depois = footer.location['y']
                self.get_posts()
                if ((antes == depois) or (numberOfPosts == thresholdPosts)):
                    break

            self.doLikesAndFollows()
        self.run(thresholdPosts)


def main():
    """Essa é a main do projeto."""

    # thresholdTimeFollow = float(
    #     input('adicione aqui o tempo de delay entre seguir e curtir (em s):'))
    # thresholdTimeLike = float(
    #     input(
    #         'adicione aqui o tempo de delay entre curtir e proxima postagem (em s):'
    #     ))
    thresholdPost = int(input('adicione aqui o limite de posts para buscar:'))

    teste = intagramBot()
    teste.run(thresholdPost)


if __name__ == '__main__':
    main()
