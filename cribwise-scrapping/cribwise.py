import requests
from bs4 import BeautifulSoup
import json
import os
import re

# URL CRIBWISE Help Center
HELP_CENTER_URL = "https://cribwise.com/help-center/"
BASE_EXPORT_PATH = os.path.join(os.getcwd(), 'help center')

def get_soup(url: str) -> BeautifulSoup:
    """
    Configura e retorna um objeto BeautifulSoup a partir de uma URL.
    
    Argumentos:
    url (str): A URL do site que você deseja analisar.
    
    Retorna:
    BeautifulSoup: Um objeto BeautifulSoup configurado com o conteúdo HTML da URL fornecida.
    None: Se ocorrer algum erro ao fazer a requisição HTTP ou analisar o conteúdo HTML.
    """
    try:
        # Fazendo a requisição HTTP para obter o conteúdo da página
        response = requests.get(url)
        # Verifica se a requisição foi bem-sucedida (status code 200)
        if response.status_code == 200:
            # Configura um objeto BeautifulSoup com o conteúdo HTML da página
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print("Erro ao fazer a requisição. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Erro ao obter o conteúdo da página:", e)
        return None

def set_hc_links(soup: BeautifulSoup) -> dict:
    elements = soup.find_all(class_="hkb-categoryhead__title")
    links = {}
    not_available = 0
    for element in elements:
        try:
            link = element.find('a').get('href')
            title = element.find('a').text
            links[title] = link
        except Exception as e:
            not_available += 1
            print('\n>>> Link not available:', element.text.strip(), f'[{not_available}]\n')
    
    # Persistencia dos links em um arquivo
    with open('help-center-links.json', 'w') as file:
        json.dump(links, file)
    
    return links if links else None

def set_article_links(soup: BeautifulSoup, old_links={}) -> dict:
    elements = soup.find_all(class_="hkb-articlepreview__title")
    if old_links == {}:
        links = old_links
    else:
        links = {}
    not_available = 0

    for element in elements:
        try:
            link = element.find('a').get('href')
            title = element.find('a').text
            links[title] = link
            print(f'\n>>> Link adicionado: {title} - {link}')
        except Exception as e:
            not_available += 1
            print('\n>>> Article Link not available:', element.text.strip(), f'[{not_available}]\n')
    
    return links if links else None

def set_full_links(help_center_links: dict) -> dict:
    article_links = {}
    for title, link in help_center_links.items():

        print(f'\n-> {title} - {link}')

        soup = get_soup(link)

        # Todos os links de um titulo
        title_links = {}

        # Coletar os links da primeira pagina
        title_links.update(set_article_links(soup))

        # Verificar a exitencia do next link
        next = soup.find(class_="next")

        while next is not None:
            soup = get_soup(next.get('href'))
            title_links.update(set_article_links(soup))
            next = soup.find(class_="next")

        article_links[title] = title_links
    
    # Persistir os Article Links
    with open('article_links.json', 'w') as f:
        try:
            json.dump(article_links, f)
            print('\n>>> Persistencia dos Article Links concluida.')
        except Exception as e:
            print(e)
    
    return article_links if article_links else None

def extract_text(links: dict):

    print('--------------------------- Articles ---------------------------')
    for folder, articles in links.items():
        print('\n------------------------------------------------------')
        if not os.path.exists(BASE_EXPORT_PATH):
            os.mkdir(BASE_EXPORT_PATH)
        if not os.path.exists(os.path.join(BASE_EXPORT_PATH, folder)):
            os.mkdir(os.path.join(BASE_EXPORT_PATH, folder))
            print(f'\nDiretório {folder} criado com sucesso\n')
        
        for title, link in articles.items():
            soup = get_soup(link)
            html_article = soup.find('div', class_='hkb-article').text

            # Regex para remover caracteres especiais do title
            title = re.sub(r'[^a-zA-Z0-9\s]', '', title)

            with open(os.path.join(BASE_EXPORT_PATH, folder, title)+'.txt', 'w', encoding='utf-8') as article:
                # Eliminar espaços extras do texto
                article.write(html_article)
                print(f'\n>>> Artigo - {title} - criado com sucesso!\n')

        print('------------------------------------------------------\n')


def run() -> dict:
    """ 
    Controls the execution of the script
    """
    # Generating soup object from URL [HELP-CENTER]
    print('\n','>>> Generating Soup Object...' ,'\n')
    soup = get_soup(HELP_CENTER_URL)

    # Coleta Links e Title da pagina [HELP-CENTER]
    print('\n','>>> Extracting HELP CENTER Links' ,'\n')
    hc_links = set_hc_links(soup)

    # Coletar Links e Title para cada Link da pagina [HELP-CENTER]
    print('\n','>>> Organizing All links together' ,'\n')
    full_links = set_full_links(hc_links)

    print('\n','>>> All links has been extraced sucessfully (articles_links.json)' ,'\n')
    return full_links


if __name__ == '__main__':

    with open('article_links.json', 'r') as article_links_file:
        links = json.load(article_links_file)
        extract_text(links)