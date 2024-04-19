import time
import os
import logging
from pychrome import Chrome
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class PythonCleaner:
    def __init__(self, diretorios_alvo, extensoes_temporarias):
        self.diretorios_alvo = diretorios_alvo
        self.extensoes_temporarias = extensoes_temporarias
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def welcome(self) -> None:
        print('******************************************************************')
        print('****************      PYTHON_CLEANER   ****************************')
        print('*******************************************************************')
        print('----------------        WELCOME        ----------------------------')
        time.sleep(3)
        print('\nCleaning .................')

    def limpar_arquivos_temporarios(self):
        """
        Limpa arquivos temporários dos diretórios alvo.
        """
        for diretorio_alvo in self.diretorios_alvo:
            try:
                with os.scandir(diretorio_alvo) as it:
                    for entrada in it:
                        if entrada.is_file() and entrada.name.endswith(tuple(self.extensoes_temporarias)):
                            caminho_arquivo = os.path.join(diretorio_alvo, entrada.name)
                            try:
                                os.remove(caminho_arquivo)
                                print(f"Arquivo removido: {caminho_arquivo}")
                                self.logger.info(f"Arquivo removido: {caminho_arquivo}")
                            except Exception as e:
                                print(f"Não foi possível remover o arquivo {caminho_arquivo}: {e}")
                                self.logger.error(f"Não foi possível remover o arquivo {caminho_arquivo}: {e}")
            except Exception as e:
                print(f"Erro ao limpar diretório {diretorio_alvo}: {e}")
                self.logger.error(f"Erro ao limpar diretório {diretorio_alvo}: {e}")

    def limpar_cache_chrome(self):
        try:
            chrome = Chrome()
            chrome.clear_cache()
            chrome.close()
            print("Cache do Google Chrome limpo.")
        except Exception as e:
            print(f"Erro ao limpar o cache do Google Chrome: {e}")

    def limpar_cookies_firefox(self):
        try:
            options = FirefoxOptions()
            options.headless = True  # Executa o navegador em modo headless (sem interface gráfica)
            driver = webdriver.Firefox(options=options)
            driver.get('about:preferences#privacy')  # Abre as configurações de privacidade do Firefox
            driver.find_element_by_id('clearOnClose-checkbox').click()  # Marca a opção de limpar cookies ao fechar
            driver.find_element_by_id('clearOnClose-checkbox').click()  # Desmarca a opção para garantir que esteja desmarcada
            driver.find_element_by_id('cookieExceptions').click()  # Abre as exceções de cookies
            driver.find_element_by_id('clearButton').click()  # Clica no botão para limpar todos os cookies
            driver.close()
            print("Cookies do Mozilla Firefox limpos.")
        except Exception as e:
            print(f"Erro ao limpar os cookies do Mozilla Firefox: {e}")

def main():
    diretorios_alvo = [
        "C:\\Windows\\Temp",  # Diretório temporário no Windows
        os.path.join(os.getenv('APPDATA'), 'Local', 'Temp')  # Diretório temporário local do usuário
    ]
    extensoes_temporarias = ['.tmp', '.temp', '.bak', '.log', '.json', '.gz', '.LOG', '.txt', '.MTX', '.Mtx']  # Adicione outras extensões conforme necessário

    cleaner = PythonCleaner(diretorios_alvo, extensoes_temporarias)
    cleaner.welcome()
    cleaner.limpar_arquivos_temporarios()
    cleaner.limpar_cache_chrome()
    cleaner.limpar_cookies_firefox()

if __name__ == "__main__":
    main()



