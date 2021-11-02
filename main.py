
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from random import randint
from time import sleep
import pytesseract
import importlib
import constants
import sys
import cv2
import os

print("Iniciando...")

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
alph = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
# alph = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
pytesseract.pytesseract.tesseract_cmd = r'.\tesseract.exe' # Substituir para o diretório de instalação https://github.com/UB-Mannheim/tesseract/wiki
soma = 0

# reconhece texto em imagens
def imgParaString(path):
    img = cv2.imread(path)
    texto = pytesseract.image_to_string(img).replace("\n", " ")
    return texto

# verifica imagem repetida
def verificarImg(path):
    if ("requesting does not exist or" in imgParaString(path)):
        return True
    elif ("was removed" in imgParaString(path)):
        return True
    elif ("Lightshot screenshot" in imgParaString(path)):
        return True
    else: return False

# gera url aleatoria
def gerarUrl():
    url = ("https://prnt.sc/")
    frase = ""
    for x in range(1, randint(4, 7)):
        frase += alph[randint(0, len(alph)-1)]
    return url+frase

# adiciona 1 a variavel encontrados
def adicionarValorEncontrados(lista):
    try:
        nomeDaLista = lista.__name__
        valorAtual = lista.encontrados
        arquivo = open(f'{nomeDaLista}.py', 'r')
        conteudo = arquivo.read()
        arquivo.close()
        arquivo2 = open(f'{nomeDaLista}.py', 'w')
        arquivo2.write(conteudo.replace(f"encontrados = {valorAtual}", f"encontrados = {valorAtual + 1}"))
        arquivo2.close()
        importlib.reload(constants)
    except Exception as e:
        print(f"Erro em {e}\nFunção adicionar valor")

# adiciona valor encontrado ao array
def adicionarAchados(lista, conta):
    try:
        nomeDaLista = lista.__name__
        achadosAtual = lista.achados
        if conta not in achadosAtual:
            conta = (f"'{conta}'")
            arquivo = open(f'{nomeDaLista}.py', 'r')
            conteudo = arquivo.read()
            arquivo.close()
            arquivo2 = open(f'{nomeDaLista}.py', 'w')
            achadosString = str(achadosAtual).replace("]", "")
            if (len(achadosAtual) == 0):
                arquivo2.write(conteudo.replace(f"achados = {achadosAtual}", f"achados = {f'{achadosString}{conta}]'}"))
            else:
                arquivo2.write(conteudo.replace(f"achados = {achadosAtual}", f"achados = {f'{achadosString}, {conta}]'}"))
            arquivo2.close()
        importlib.reload(lista)
    except Exception as e:
        print(f"Erro em {e}\nFunção adicionar array")

def main():
    global soma
    soma = 0
    if constants.encontrados != 0:
        for x in range(len(constants.achados)):
            soma += len(constants.achados[x])
    try:
        url = gerarUrl()
        driver.get(url) # link completo
        comp = url.replace("https://prnt.sc/", "")
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="screenshot-image"]')))
        sleep(2) # esperar imagem carregar
        with open(f'./imagens/{comp}.png', 'wb') as file:
            file.write(driver.find_element_by_xpath('/html/body/div[3]/div/div/img').screenshot_as_png)
        if (verificarImg(f"./imagens/{comp}.png") == True):
            os.remove(f"./imagens/{comp}.png")
        elif comp in constants.achados:
            os.remove(f"./imagens/{comp}.png")
            print(f"Encontrado, duplicado.\n{url}")
        else:
            adicionarAchados(constants, comp)
            adicionarValorEncontrados(constants)
    except Exception as e:
        if (driver.current_url == "https://prnt.sc/"):
            pass
        else:
            print(e)
            input(f"\nErro em\n{e}\nPressione ENTER para finalizar.\n")
            driver.quit()

# verifica se a pasta 'imagens' existe
if os.path.isdir('./imagens') == False:
    print("A pasta './imagens' não existe, criando...")
    os.mkdir('./imagens')

while True:
    try:
        main()
        os.system('cls' if os.name == 'nt' else 'clear')
        if constants.encontrados != 0:
            print(f"Total de imagens encontradas: {constants.encontrados}\nMédia de caracteres por URL: {round(soma/constants.encontrados)}")
        else:
            print(f"Total de imagens encontradas: {constants.encontrados}")
        print("\nPara finalizar utilize CTRL + C")
    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Encerrando, aguarde...")
        driver.quit()
        input("Finalizado.")
        sys.exit()