"""
scraper_precos.py
=================
Monitor de preços via Web Scraping.

Percorre um catálogo de produtos na web, extrai os dados de cada item
(título, preço, avaliação e disponibilidade), navega automaticamente por
todas as páginas e exporta o resultado para **CSV** e **Excel**.

O alvo padrão é o site https://books.toscrape.com — um site público criado
especificamente para praticar web scraping (uso livre e legal). A mesma
técnica se aplica a qualquer e-commerce; basta adaptar os seletores.

Uso:
    py scraper_precos.py                 # varre todas as páginas
    py scraper_precos.py --paginas 5     # apenas as 5 primeiras páginas
    py scraper_precos.py --saida dados   # nomes de saída (dados.csv/.xlsx)

Autor: Bruno Porto
Dependências: requests, beautifulsoup4, lxml, pandas, openpyxl
"""

import argparse
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://books.toscrape.com/catalogue/page-1.html"

# Cabeçalho educado: identifica o bot em vez de fingir ser um navegador comum.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PortfolioScraper/1.0; estudo de web scraping)"
}

# Conversão da classe CSS de estrelas para número
ESTRELAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def buscar_pagina(url: str, sessao: requests.Session) -> BeautifulSoup:
    """Baixa uma página e devolve o HTML já parseado."""
    resposta = sessao.get(url, headers=HEADERS, timeout=20)
    resposta.raise_for_status()
    resposta.encoding = resposta.apparent_encoding  # garante acentos corretos
    return BeautifulSoup(resposta.text, "lxml")


def extrair_produtos(sopa: BeautifulSoup, url_pagina: str) -> list[dict]:
    """Extrai a lista de produtos de uma página de catálogo."""
    produtos = []
    for item in sopa.select("article.product_pod"):
        titulo = item.h3.a["title"].strip()

        preco_txt = item.select_one("p.price_color").get_text(strip=True)
        # "£51.77" -> 51.77
        preco = float(preco_txt.replace("£", "").replace("Â", "").strip())

        classe_estrela = item.select_one("p.star-rating")["class"]
        # ['star-rating', 'Three'] -> 3
        avaliacao = next((ESTRELAS[c] for c in classe_estrela if c in ESTRELAS), None)

        disponibilidade = item.select_one("p.instock.availability").get_text(strip=True)

        link_rel = item.h3.a["href"]
        link = urljoin(url_pagina, link_rel)

        produtos.append({
            "titulo": titulo,
            "preco_gbp": preco,
            "avaliacao_estrelas": avaliacao,
            "disponibilidade": disponibilidade,
            "link": link,
        })
    return produtos


def proxima_pagina(sopa: BeautifulSoup, url_atual: str) -> str | None:
    """Descobre a URL da próxima página, ou None se acabou."""
    botao = sopa.select_one("li.next a")
    if not botao:
        return None
    return urljoin(url_atual, botao["href"])


def coletar(url_inicial: str, max_paginas: int | None, atraso: float) -> pd.DataFrame:
    """Percorre o catálogo página a página e devolve um DataFrame."""
    sessao = requests.Session()
    todos = []
    url = url_inicial
    pagina = 1

    while url:
        print(f"  Página {pagina}: {url}")
        sopa = buscar_pagina(url, sessao)
        produtos = extrair_produtos(sopa, url)
        todos.extend(produtos)
        print(f"    -> {len(produtos)} produtos extraídos (total: {len(todos)})")

        if max_paginas and pagina >= max_paginas:
            break

        url = proxima_pagina(sopa, url)
        pagina += 1
        if url:
            time.sleep(atraso)  # pausa educada entre requisições

    return pd.DataFrame(todos)


def exportar(df: pd.DataFrame, base_saida: Path) -> None:
    """Salva os dados em CSV e Excel."""
    csv_path = base_saida.with_suffix(".csv")
    xlsx_path = base_saida.with_suffix(".xlsx")

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False, sheet_name="Produtos")

    print(f"  -> CSV  salvo em: {csv_path.name}")
    print(f"  -> Excel salvo em: {xlsx_path.name}")


def resumir(df: pd.DataFrame) -> None:
    """Imprime um pequeno resumo dos dados coletados."""
    if df.empty:
        print("  Nenhum produto coletado.")
        return
    print("\nResumo da coleta:")
    print(f"  Total de produtos : {len(df)}")
    print(f"  Preço médio       : £{df['preco_gbp'].mean():.2f}")
    print(f"  Mais barato       : £{df['preco_gbp'].min():.2f}")
    print(f"  Mais caro         : £{df['preco_gbp'].max():.2f}")
    print(f"  Avaliação média   : {df['avaliacao_estrelas'].mean():.1f} estrelas")


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor de preços via web scraping.")
    parser.add_argument("--paginas", type=int, default=None,
                        help="Número máximo de páginas (padrão: todas)")
    parser.add_argument("--atraso", type=float, default=0.5,
                        help="Pausa em segundos entre páginas (padrão: 0.5)")
    parser.add_argument("--saida", default="precos_coletados",
                        help="Nome-base dos arquivos de saída")
    args = parser.parse_args()

    print("Iniciando coleta de preços...")
    df = coletar(URL_BASE, args.paginas, args.atraso)

    base_saida = Path(__file__).parent / args.saida
    exportar(df, base_saida)
    resumir(df)
    print("\nConcluído!")


if __name__ == "__main__":
    main()
