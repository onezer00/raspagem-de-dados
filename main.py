from collections import OrderedDict
import re

from alive_progress import alive_bar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


url = 'https://crmpb.org.br/busca-medicos/'
timeout = 30

list_of_columns = ['Nome', 'CRM', 'Data de Inscrição', 'Primeira inscrição na UF', 'Inscrição', 'Situação', 'Inscrições em outro estado', 'Especialidades/Áreas de Atuação', 'Endereço', 'Telefone']

with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, timeout)
    driver.set_script_timeout(30)
    driver.get(url)

    # click in button to get doctors
    driver.find_element(By.CSS_SELECTOR, "button.button").click()
    driver.find_element(By.CSS_SELECTOR, "button.btn-buscar.btnPesquisar").click()

    result_text = None

    result_pagination = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'paginationjs-last')))
    total_pages = int(result_pagination.text)

    pages = input('Digite a quantidade de páginas que deseja buscar ou "All" para toddas as páginas: ')
    if pages.lower() != 'all':
        total_pages = int(pages)

    nova_tabela_list = []
    page = 1
    while page < total_pages:
        # Encontra todos os botões de paginação
        pagination_buttons = driver.find_elements(By.CLASS_NAME, 'paginationjs-page')
        # Encontra o botão da próxima página
        next_page_button = None
        for button in pagination_buttons:
            if button.get_attribute('data-num') == str(page + 1):
                next_page_button = button
                break
    
        # Clica no botão da próxima página se ele existir
        if next_page_button:
            # Pega a tabela apenas para verificar o tamanho
            tabela = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'busca-resultado')))
            tabela_linhas = tabela.text.split('\n')
            with alive_bar(len(tabela_linhas)) as line:
                size_table = len(tabela_linhas)
                execute_block = True
                for linha in range(0, size_table):
                    # Preciso verificar se o bloco de código precisa ser executado ou não
                    if execute_block:
                        if linha == len(tabela_linhas) - 1:
                            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'busca-resultado')))
                        if not re.findall(r'(.+): (.+)', tabela_linhas[linha]):
                            # Separa a chave e o valor
                            if ':' in tabela_linhas[linha] or tabela_linhas[linha][0] == ' ':
                                key = tabela_linhas[linha][:-1]
                                if linha + 1 < len(tabela_linhas) and(tabela_linhas[linha].lstrip() != re.findall(r'(.+): (.+)', nova_tabela_list[-1])[0][1]):
                                    n = 1
                                    if len(re.findall(r'(.+): (.+)', tabela_linhas[linha + n].lstrip())) > 0:
                                        while re.findall(r'(.+): (.+)', tabela_linhas[linha + n].lstrip())[0][0] not in list_of_columns:
                                            value += ', ' + tabela_linhas[linha + n].lstrip()
                                            n += 1
                                    else:
                                        value = tabela_linhas[linha + 1].lstrip()
                                    print(f'{key}: {value}')
                                    nova_tabela_list.append(f'{key}: {value}')
                                    execute_block = False

                                elif key[0] != ' ':
                                    print(f'{key}:')
                                    nova_tabela_list.append(key)
                            else:
                                nome = tabela_linhas[linha]
                                print(f'\n{nome}')
                                nova_tabela_list.append(nome)
                        else:
                            # Separa chave e valor até que o próximo não possa ser separado
                            key, value = re.findall(r'(.+): (.+)', tabela.text.split('\n')[linha])[0]
                            if key in list_of_columns:
                                print(f'{key}: {value}')
                                nova_tabela_list.append(f'{key}: {value}')
                        # Caso o bloco de código acima não seja executado, preciso executar o loop na próxima iteração
                        line()
                    else:
                        execute_block = True
                        
                next_page_button.click()
                print(f'\n\nAguardando carregamento da próxima página {page}...\n\n')
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'busca-resultado')))
            page += 1
        # Exportar dados para planilha do Excel
        if page == total_pages:
            result = []
            current_name = None

            for i in range(0, len(nova_tabela_list)):
                if ':' not in nova_tabela_list[i]:
                    current_name = nova_tabela_list[i]
                    result.append({'Nome': current_name})
                else:
                    key, value = nova_tabela_list[i].split(': ', maxsplit=1)
                    if key == 'Telefone':
                        if 'Inscrições em outro estado' not in result[-1].keys():
                            result[-1].update({'Inscrições em outro estado': 'Não informado'})
                            # converter o OrderedDict para lista
                            items = list(result[-1].items())
                            # inserir a chave na posição desejada
                            items.insert(6, ('Inscrições em outro estado', 'Não informado'))
                            # converter de volta para OrderedDict
                            result[-1] = dict(OrderedDict(items))
                        result[-1][key] = value
                    else:
                        result[-1][key] = value

            # Criando um dataframe com os dados e salvando em um arquivo Excel
            df = pd.DataFrame.from_dict(result, orient='columns')
            df.to_excel('dados.xlsx', index=False)

driver.quit()
