import requests
import bs4
import fake_headers
import json
URL = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

def gen_headers():
    headers_gen = fake_headers.Headers(browser="chrome", os="win")
    return headers_gen.generate()

response = requests.get(URL, headers=gen_headers())
main_html = response.text
good_vacancies = []
main_page = bs4.BeautifulSoup(main_html, "lxml")
all_vacancies_tag = main_page.find("div", attrs={"data-qa": "vacancy-serp__results"})
vac_tags = all_vacancies_tag.find_all("div", class_="vacancy-serp-item__layout")
for article_tag in vac_tags:
    span_tag = article_tag.find("span", class_="serp-item__title")
    work_name = span_tag.text.strip()
    if "Django" in work_name and "Flask" in work_name:
        good_vacancias = {}
        good_vacancias["vacancy_name"] = work_name
        # Название компании
        company_name_tag = article_tag.find("a", attrs={"data-qa": "vacancy-serp__vacancy-employer"})
        company_name = company_name_tag.text
        if 'ООО ' in company_name:
            company_name = f"OOO {company_name[4:]}"
        good_vacancias["company_name"] = company_name
        # Адрес
        address_tag = article_tag.find("div", attrs={"data-qa": "vacancy-serp__vacancy-address"})
        address = address_tag.text
        good_vacancias["address"] = address
        # Зарплата
        salary_tag = article_tag.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
        if salary_tag != None:
            salary = salary_tag.text.replace('\u202f', ' ').strip()
            good_vacancias["salary"] = salary
        # Ссылка
        url_work_tag = article_tag.find("a", class_="bloko-link")
        url_work = url_work_tag.attrs.get("href")
        good_vacancias["url"] = url_work
        good_vacancies.append(good_vacancias)

print(good_vacancies)
with open("vacancies.json", "w", encoding="utf-8") as file:
    json.dump(good_vacancies, file, indent=4, ensure_ascii=False)