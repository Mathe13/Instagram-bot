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

    def doLogin(self):
        print('Do login')
        self.driver.get('https://www.instagram.com/accounts/login/')
        # self.wait(5)
        while True:
            try:
                input_name = self.driver.find_element(By.NAME, 'username')
                input_senha = self.driver.find_element(By.NAME, 'password')
                login_button = self.driver.find_element(
                    By.CSS_SELECTOR, '._qv64e')

                if login_button.is_enabled() and input_name.is_enabled(
                ) and input_senha.is_enabled():
                    break
            except:
                pass

        input_name.send_keys(name)
        input_senha.send_keys(senha)
        login_button.click()

        print('\tsend form login')

        while True:
            url_now = self.driver.current_url
            if url_now == 'https://www.instagram.com/':
                break

    def doLogout(self):
        self.driver.get("https://www.instagram.com/" + name + "/")
        self.wait(5)
        self.driver.find_element_by_css_selector('._q8y0e').click()
        # botão q abre o modal de logout
        self.wait(2)
        botoes = self.driver.find_elements_by_css_selector('._o2wxh > button')
        botoes[3].click()


# self.driver.get("https://www.instagram.com/" + name + "/")
# # self.wait(5)
# while True:
#     try:
#         modal_button = self.driver.find_elements_by_css_selector(
#             '._q8y0e')
#         if modal_button.is_enabled():
#             break
#     except:
#         print('passing1')
#
# modal_button.click()
# # botão q abre o modal de logout
# # self.wait(2)
# while True:
#     try:
#         botoes = self.driver.find_elements_by_css_selector(
#             '._o2wxh > button')
#         if botoes.is_enabled():
#             break
#     except:
#         print('passing2')
# botoes[3].click()

    def takeTopHashtags(self):
        """Pega as # dispoiveis no dom"""
        self.driver.get('https://top-hashtags.com/instagram/')
        print('take top #')
        raw = self.driver.find_elements_by_css_selector(
            '.tht-tag.small-7.medium-9.columns>a')
        self.qtdHashtags = 0
        if raw:
            print('\ttop #')
            for hashtag in raw:
                self.qtdHashtags += 1
                self.hashtags.append(hashtag.text)
                print("\t\t" + str(self.qtdHashtags) + ": " + hashtag.text)
        else:
            print('\tNenhuma # encontrada')

    def scroll_page(self, direction, tempo=3):
        """Dá um scroll na pagina."""
        print('\tscroll ' + direction + ' e espera ' + str(tempo))
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

    def get_posts(self, thresholdPosts):
        """Pega o link dos post disponiveis no dom."""
        print('get the posts')
        raw = self.driver.find_elements_by_css_selector(
            '._mck9w._gvoze._tn0ps>a')
        if raw:
            print('\tGet the links of the posts')
            for post in raw:
                self.numberOfPosts += 1
                self.posts.append(post.get_attribute('href'))
                if (thresholdPosts <= self.numberOfPosts):
                    break
        else:
            print(
                'Nenhum Post encontrado, Verifique se é uma hashtag utilizada')

    def doLikesAndFollows(self):
        print('Exec doLikesAndFollows')
        print(
            '\tQuantidade de links a ser processados: ' + str(len(self.posts)))
        if (self.posts):
            i = 0
            for post in self.posts:
                i += 1
                print('\t\tPost ' + str(i) + '\n\t\t\tLink: ' + post)
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

                if (pageErr == False):
                    try:
                        followed = self.driver.find_element_by_css_selector(
                            '._qv64e._jqf0k._4tgw8._njrw0'
                        )  # Se encontrar significa q ja está followed
                        print('\t\t\tThis profile has been follow')
                    except:
                        followed = False

                    if (followed == False):
                        follow_button = self.driver.find_element_by_css_selector(
                            '._qv64e._iokts._4tgw8._njrw0'
                        )  # botao de seguir //isto é um buttom (tag buttun)
                        followed = True
                        while True:
                            if follow_button.is_enabled():
                                break
                        follow_button.click()
                        inicio = time.time()

                        while True:
                            try:
                                followed_button = self.driver.find_element_by_css_selector(
                                    '._qv64e._jqf0k._4tgw8._njrw0')
                                if followed_button.is_enabled():
                                    print('\t\t\tFollowed @' + str(
                                        self.driver.
                                        find_element_by_css_selector(
                                            '._eeohz>a._2g7d5.notranslate._iadoq'
                                        ).text))
                                    break
                            except:
                                if time.time(
                                ) - inicio > 5:  # se nao mudou em 5 segundos, vai pro proximo, normalmente se nao mudou é pq que levou block follow
                                    print('\t\t\tDo the logout')
                                    url_now = self.driver.current_url
                                    self.doLogout()
                                    print('\t\t\tRestart the window')
                                    self.driver.close()
                                    self.driver = webdriver.Firefox()
                                    print('\t\t\tDo the login')
                                    self.doLogin()
                                    print('\t\t\tGo back for the post')
                                    self.driver.get(url_now)
                                    break
                                pass

                    try:
                        liked = self.driver.find_element_by_css_selector(
                            '._eszkz._l9yih>span._8scx2.coreSpriteHeartFull'
                        )  # se encontrar significa que ainda n foi curtido
                        print('\t\t\tThis photo is already there')
                    except:
                        liked = False

                    if (liked == False):
                        like_button = self.driver.find_element_by_css_selector(
                            '._eszkz._l9yih'
                        )  # botao de like //isto é um link (uma tag a)
                        liked = True
                        while True:
                            if like_button.is_enabled():
                                break
                        like_button.click()

                        print('\t\t\tLiked the photo')

                    while True:
                        if not self.verify_if_is_liked() == False:
                            break

    def verify_if_is_liked(self):
        try:
            liked = self.driver.find_element_by_css_selector(
                '._eszkz._l9yih>span._8scx2.coreSpriteHeartFull'
            )  # se encontrar significa que ainda n foi curtido
        except:
            return False
        return True

    def unfollow_all(self):
        print('Unfollowing all')
        self.driver.get('https://www.instagram.com/' + name + '/')
        # self.wait(1)
        while True:
            try:
                following_button = self.driver.find_elements_by_css_selector(
                    '._t98z6')
                following_number = self.driver.find_elements_by_css_selector(
                    '._t98z6 > span')
                if following_button.is_enabled(
                ) and following_number.is_enabled():
                    break
            except:
                pass

        print('\tclickando')
        following_button[2].click()
        while True:
            try:
                modal_open = self.driver.find_element_by_css_selector(
                    '._784q7._3g81g')
                if modal_open.is_enabled():
                    print('\tThe model for unfollow is open')
                    break
            except:
                pass

        # self.wait(2)
        if not (following_number == 0):
            unfollow_buttons = self.driver.find_elements_by_css_selector(
                '._qv64e._t78yp._4tgw8._njrw0')
            for unfollow_button in unfollow_buttons:
                unfollow_button.click()
                while True:
                    if unfollow_button.is_enabled():
                        break
                # self.wait(2)
        self.unfollow_all()

    def run(self, thresholdPosts):
        self.doLogin()
        self.posts = []
        self.qtdHashtags = 0

        for hashtag in self.hashtags:
            try:
                self.driver.get(
                    'https://www.instagram.com/explore/tags/' + hashtag[1:])
            except Exception as e:
                print('erro ao abrir link')
                self.error_details(e)

            footer = self.driver.find_element(By.TAG_NAME, 'footer')
            self.numberOfPosts = 0
            self.qtdHashtags += 1
            print('Select ' + hashtag + ' number ' + str(self.qtdHashtags) +
                  ' of the list')
            while True:

                antes = footer.location['y']
                self.scroll_page(direction='Down', tempo=1)
                depois = footer.location['y']
                self.get_posts(thresholdPosts)
                if ((antes == depois)
                        or (self.numberOfPosts >= thresholdPosts)):
                    break

            self.doLikesAndFollows()
            self.posts = []
        self.run(thresholdPosts)


def main():
    """Essa é a main do projeto."""

    #thresholdTimeFollow = float(input('adicione aqui o tempo de delay entre seguir e curtir (em s):'))
    #thresholdTimeLike = float(input('adicione aqui o tempo de delay entre curtir e proxima postagem (em s):'))
    thresholdPost = int(input('adicione aqui o limite de posts para buscar:'))

    teste = intagramBot()
    teste.run(thresholdPost)


if __name__ == '__main__':
    main()
