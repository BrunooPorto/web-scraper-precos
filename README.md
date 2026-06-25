# 🔎 Monitor de Preços via Web Scraping

Script em **Python** que percorre um catálogo de produtos na web, extrai
**título, preço, avaliação e disponibilidade** de cada item, navega
automaticamente por **todas as páginas** e exporta tudo para **CSV e Excel**.

> Útil para quem precisa monitorar preços de concorrentes, montar catálogos
> ou coletar dados de produtos sem copiar e colar manualmente.

---

## ✨ O que ele faz

- Navega automaticamente por **todas as páginas** do catálogo (paginação)
- Extrai, de cada produto: **título, preço, avaliação (estrelas) e estoque**
- Exporta o resultado em **`.csv`** e **`.xlsx`** prontos para análise
- Mostra um **resumo** no fim: total, preço médio, mais barato/caro, nota média
- É **educado**: usa pausa entre requisições e um `User-Agent` identificável

---

## 🚀 Como usar

```bash
# 1. Instale as dependências
pip install requests beautifulsoup4 lxml pandas openpyxl

# 2. Rode o script (varre todas as páginas)
python scraper_precos.py

# Ou limite a quantidade de páginas (mais rápido para testar):
python scraper_precos.py --paginas 5
```

Saída padrão: `precos_coletados.csv` e `precos_coletados.xlsx`.

### Opções

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `--paginas` | Nº máximo de páginas a varrer | todas |
| `--atraso`  | Pausa (segundos) entre páginas | 0.5 |
| `--saida`   | Nome-base dos arquivos de saída | `precos_coletados` |

---

## 🛠️ Tecnologias

- **Python 3.10+**
- **requests** — download das páginas
- **BeautifulSoup + lxml** — extração dos dados do HTML
- **pandas + openpyxl** — exportação para CSV e Excel

---

## ⚖️ Uso responsável

O alvo padrão é **[books.toscrape.com](https://books.toscrape.com)**, um site
público criado **especificamente para praticar web scraping**. A mesma técnica
se aplica a sites reais — sempre **respeitando os Termos de Uso, o `robots.txt`
e um intervalo educado entre requisições**.

---

## 💡 Sobre

Projeto de portfólio focado em **coleta e estruturação de dados da web**.
Posso adaptar o scraper ao site que você precisa, agendar coletas periódicas,
detectar mudanças de preço e enviar alertas por e-mail ou Telegram.

📬 **Precisa monitorar preços ou coletar dados de algum site? Vamos conversar!**
