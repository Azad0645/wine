from collections import defaultdict
import pandas as pd
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def age_with_suffix(age):
    if 10 <= age % 100 <= 20:
        suffix = "лет"
    elif age % 10 == 1:
        suffix = "год"
    elif 2 <= age % 10 <= 4:
        suffix = "года"
    else:
        suffix = "лет"
    return f"{age} {suffix}"


df = pd.read_excel(
    'wine3.xlsx',
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
winery_age_display = age_with_suffix(winery_age)


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