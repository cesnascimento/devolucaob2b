from functools import lru_cache
import requests
from bs4 import BeautifulSoup
import re
from app_control.utils import correios_sedex


cookies = {
    'CFID': 'Z2zupw17sx0mb9c8bxwecblmh2vu4f5bkqznfhwe1sftit2te7n-226488339',
    'CFTOKEN': 'Z2zupw17sx0mb9c8bxwecblmh2vu4f5bkqznfhwe1sftit2te7n-56d8fb4d404b7872-F481511E-03D2-9065-E02188169BE03973',
    'CFGLOBALS': 'urltoken%3DCFID%23%3D226488339%26CFTOKEN%23%3D56d8fb4d404b7872%2DF481511E%2D03D2%2D9065%2DE02188169BE03973%26jsessionid%23%3D7EB5AE79466A8EB0CED58B55F5405A09%2Ecfusion01%23lastvisit%3D%7Bts%20%272023%2D03%2D10%2010%3A12%3A15%27%7D%23hitcount%3D2%23timecreated%3D%7Bts%20%272023%2D03%2D10%2010%3A12%3A15%27%7D%23cftoken%3D56d8fb4d404b7872%2DF481511E%2D03D2%2D9065%2DE02188169BE03973%23cfid%3D226488339%23',
    '_ga_ENTETZ55ME': 'GS1.1.1678471635.1.0.1678471641.0.0.0',
    '_ga': 'GA1.3.705872291.1677161943',
    '_ga_J59GSF3WW5': 'GS1.1.1679934936.11.0.1679934936.0.0.0',
    'CFID': '1060043',
    'CFTOKEN': '3c11d625e89e46ed%2DDCB24367%2DBD56%2DD12B%2DC68B0F27456A3262',
    'dtCookie': 'v_4_srv_3_sn_88CE0D9E70C06FA85F309EEE49457BA5_perc_100000_ol_0_mul_1_app-3Aacb4ccc372c47f00_0',
    'LBprdint2': '140052490.20480.0000',
    'LBprdExt2': '801701898.47873.0000',
    'TS017d8577': '01ff9e5fc6a6224d09317258bde82c8cc7032221b7e25ac4bb08b4873495cf8dd76e419a39561960724adf99087b5c42a89c40ed6ce68b8d9ee78deec94b6c60ef0ba6c4c0',
    'JSESSIONID': '34D169682484C5F6BAD7A1C0F5763F24.cfusion01',
    'TS0148b1bd': '01ff9e5fc6e9655aacb4c6f70c5819ae066968a9deed8faaca85ba1b3b769e9d06856ca43f0999746ce26461739123fec6771fdf3acf6d2e153b79c90d2418726f110e9f94d60028b4199132539326595d8083a770626bafa86bcd81c03faccc65debdf55a9e299d2c120975d8fda2b65ea77eb22f91d9d4b83d5de8a95ecf1bfad31161308ac22cdffed46bbff21a204082cc857742268e693ab729e637ced29ad60275c7',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'CFID=Z2zupw17sx0mb9c8bxwecblmh2vu4f5bkqznfhwe1sftit2te7n-226488339; CFTOKEN=Z2zupw17sx0mb9c8bxwecblmh2vu4f5bkqznfhwe1sftit2te7n-56d8fb4d404b7872-F481511E-03D2-9065-E02188169BE03973; CFGLOBALS=urltoken%3DCFID%23%3D226488339%26CFTOKEN%23%3D56d8fb4d404b7872%2DF481511E%2D03D2%2D9065%2DE02188169BE03973%26jsessionid%23%3D7EB5AE79466A8EB0CED58B55F5405A09%2Ecfusion01%23lastvisit%3D%7Bts%20%272023%2D03%2D10%2010%3A12%3A15%27%7D%23hitcount%3D2%23timecreated%3D%7Bts%20%272023%2D03%2D10%2010%3A12%3A15%27%7D%23cftoken%3D56d8fb4d404b7872%2DF481511E%2D03D2%2D9065%2DE02188169BE03973%23cfid%3D226488339%23; _ga_ENTETZ55ME=GS1.1.1678471635.1.0.1678471641.0.0.0; _ga=GA1.3.705872291.1677161943; _ga_J59GSF3WW5=GS1.1.1679934936.11.0.1679934936.0.0.0; CFID=1060043; CFTOKEN=3c11d625e89e46ed%2DDCB24367%2DBD56%2DD12B%2DC68B0F27456A3262; dtCookie=v_4_srv_3_sn_88CE0D9E70C06FA85F309EEE49457BA5_perc_100000_ol_0_mul_1_app-3Aacb4ccc372c47f00_0; LBprdint2=140052490.20480.0000; LBprdExt2=801701898.47873.0000; TS017d8577=01ff9e5fc6a6224d09317258bde82c8cc7032221b7e25ac4bb08b4873495cf8dd76e419a39561960724adf99087b5c42a89c40ed6ce68b8d9ee78deec94b6c60ef0ba6c4c0; JSESSIONID=34D169682484C5F6BAD7A1C0F5763F24.cfusion01; TS0148b1bd=01ff9e5fc6e9655aacb4c6f70c5819ae066968a9deed8faaca85ba1b3b769e9d06856ca43f0999746ce26461739123fec6771fdf3acf6d2e153b79c90d2418726f110e9f94d60028b4199132539326595d8083a770626bafa86bcd81c03faccc65debdf55a9e299d2c120975d8fda2b65ea77eb22f91d9d4b83d5de8a95ecf1bfad31161308ac22cdffed46bbff21a204082cc857742268e693ab729e637ced29ad60275c7',
    'Origin': 'https://www2.correios.com.br',
    'Pragma': 'no-cache',
    'Referer': 'https://www2.correios.com.br/encomendas/servicosonline/logisticaReversa/consultas/default.cfm?t=A&m=',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


@lru_cache(maxsize=32)
def correios_postagem(post_code: str) -> str:
    data = {
    'codAdministrativo': '13365398',
    'param01': '',
    'param02': '',
    'param03': '',
    'col_aut': 'A',
    'col_mod': '',
    'gerarArquivoTexto': '0',
    'controle': '',
    'cartao': '',
    'tipo': '6',
    'objeto': f'{post_code}',
    'periodo': '',
    'data1': '',
    'data2': '',
    'cCol': [
        '1',
        '2',
        '3',
        '50',
        '20',
    ],
}
    response = requests.post(
    'https://www2.correios.com.br/encomendas/servicosonline/logisticaReversa/consultas/resultado.cfm?xest=false?requestimeout=600',
    cookies=cookies,
    headers=headers,
    data=data,
)
    print('Logger: Iniciando scraper postagem', post_code)
    soup = BeautifulSoup(response.text, 'html.parser')


    """ # Encontrando a linha desejada na tabela
    linha_desejada = soup.find('tr', class_='cssLinhaTitulo').find_next_sibling('tr')

    # Extraindo o texto formatado da linha desejada
    linha_texto = linha_desejada.get_text(strip=True)

    # Exibindo a linha em formato de texto
    print(linha_texto)

    padrao_codigo = r'\d+'
    padrao_situacao = r'[A-Za-z\s]+'
    padrao = r"OV.*?BR"

    # Aplicando os padrões de regex na string
    codigo = re.search(padrao_codigo, linha_texto).group()
    situacao = re.search(padrao_situacao, linha_texto).group()
    resultado = re.findall(padrao, linha_texto) """
    td_tags = soup.find_all('td')[1:]
    lista_td = [td.get_text(strip=True) for td in td_tags]

    codigo, situacao, resultado = lista_td[7], lista_td[8], lista_td[10]
    try:
        print("Código: ", codigo)
        print("Situação: ", situacao)
        print("Sedex: ", resultado)
        request = correios_sedex(resultado)
        print("Request: ", request)
        if resultado:
            return resultado
        else:
            print("Rastreio não encontrado.")
            return f"{codigo} ({situacao})"
    except AttributeError:
        return 'Ainda não postado'
    except Exception as e:
        return f'Erro: {e}'