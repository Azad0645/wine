import argparse
from collections import defaultdict
import pandas as pd
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def format_age_with_suffix(age):
    if 10 <= age % 100 <= 20:
        suffix = "лет"
    elif age % 10 == 1:
        suffix = "год"
    elif 2 <= age % 10 <= 4:
        suffix = "года"
    else:
        suffix = "лет"
    return f"{age} {suffix}"


def main():
    parser = argparse.ArgumentParser(description="Wine catalog site generator")
    parser.add_argument(
        "--excel",
        type=str,
        default="catalog.xlsx",
        help="Путь к Excel-файлу с каталогом (по умолчанию catalog.xlsx)"
    )
    args = parser.parse_args()

    df = pd.read_excel(
        args.excel,
        engine='openpyxl',
        na_values=[],
        keep_default_na=False
    )
    wines = df.to_dict(orient='records')

    wines_by_category = defaultdict(list)
    for wine in wines:
        category = wine["Категория"]
        wines_by_category[category].append(wine)

    foundation_year = 1920
    current_year = datetime.now().year
    winery_age = current_year - foundation_year
    winery_age_display = format_age_with_suffix(winery_age)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template("template.html")
    rendered_page = template.render(wines_by_category=wines_by_category, winery_age=winery_age_display)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()