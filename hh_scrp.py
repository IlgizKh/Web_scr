# Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург". Эти параметры задаются по ссылке
# Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
# Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.

# <div data-qa="vacancy-serp__results" id="a11y-main-content">
# <div class="serp-item" data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus">




import json
import bs4
import fake_headers
import requests
from pprint import pprint

headers = fake_headers.Headers(browser="chrome", os="win")
headers_dict = headers.generate()

response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_dict)
main_html_data = response.text
main_html = bs4.BeautifulSoup(main_html_data, "lxml")

vacancy_tags = main_html.find_all("div", class_="serp-item")
data = {}
vac_list = []
for vacancy in vacancy_tags:

    name_tag = vacancy.find("a")
    h3_tag = vacancy.find("h3")
    span_tag = h3_tag.find("span")
    a_tag = span_tag.find("a")
    if vacancy.find("span", class_="bloko-header-section-3"):
         salary = vacancy.find("span", class_="bloko-header-section-3").get_text()  #зп
         salary = salary.replace(u"\u202F", " ")
    else: salary = "NO salary"
    if vacancy.find("div", class_="bloko-text"):
         company_name = vacancy.find("div", class_="bloko-text").get_text()
         company_name = company_name.replace('\xa0', " ")  #название компании
    else: company_name = "NO name"
    if vacancy.find("div", class_="vacancy-serp-item__info"):
         company_address = list(vacancy.find("div", class_="vacancy-serp-item__info").children)[1].get_text()  # адрес компании
    else: company_address = "NO address"

    title = a_tag.text                             #название вакансии (не пустое)
    link = a_tag['href']                            #ссылка на вакансию

    response = requests.get(link, headers=headers.generate()).text
    vacancy_descr_html = bs4.BeautifulSoup(response, "lxml")
    if vacancy_descr_html.find("div", class_="g-user-content"):
         vacancy_descr_text = vacancy_descr_html.find("div", class_="g-user-content").get_text()   #описание вакансии
    else: vacancy_descr_text = "нет описания"


    if ("Django" or  "Flask") in vacancy_descr_text:
            vac_list.append({"link":link, "title":title, "salary":salary, "name":company_name, "address":company_address})


    print(link)
    print(title)
    print(salary)
    print(company_name)
    print(company_address)
with open("vacancy.json", "a", encoding="utf8") as f:
  data["vacancy"] = vac_list
  json.dump(data, f, ensure_ascii=False, indent=2)