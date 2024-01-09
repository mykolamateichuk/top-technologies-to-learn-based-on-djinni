import scrapy
from scrapy import Selector
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.common.by import By

from ..technologies import TECHNOLOGIES

ENGLISH_LEVELS_DJINNI = [
    "No English",
    "Beginner/Elementary",
    "Pre-Intermediate",
    "Intermediate",
    "Upper-Intermediate",
    "Advanced/Fluent"
]

EXPERIENCE_YEARS_DJINNI = {
    "Без досвіду": "No experience",
    "1 рік досвіду": "1 year",
    "2 роки досвіду": "2 years",
    "3 роки досвіду": "3 years",
    "5 років досвіду": "5 years"
}


class DjinniSpider(scrapy.Spider):
    name = "djinni"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome()

    def close(self, reason):
        self.driver.close()

    def parse(self, response: Response, **kwargs):
        for vacancy in response.css("main .list-jobs .list-jobs__item"):
            english_level = (vacancy
                             .css(".job-list-item__job-info .nobr::text")[-1]
                             .get()
                             .strip())

            experience_years = (vacancy
                                .css(".job-list-item__job-info .nobr::text")[-2]
                                .get()
                                .strip())

            views_and_applications = (vacancy.css(".text-muted .nobr")[1]
                                      .css(".mr-2::attr(title)").getall())

            number_of_views = int(views_and_applications[0].split()[0])
            number_of_applications = int(views_and_applications[1].split()[0])

            percentage_of_applications = round(
               number_of_applications / number_of_views, 2
            ) * 100

            if english_level not in ENGLISH_LEVELS_DJINNI:
                english_level = "Not stated"

            experience_years = (EXPERIENCE_YEARS_DJINNI
                                .get(experience_years, "Not stated"))

            detail_data = self.__parse_detailed_vacancy(response, vacancy)

            yield {
                "vacancy_name": (vacancy.css(".job-list-item__link::text")
                                 .get()
                                 .strip()),
                "location_text": (vacancy.css(".location-text::text")
                                  .get()
                                  .strip()
                                  .replace("\t", "")
                                  .replace("\n", "")
                                  .replace("    ", " ")),
                "english_level": english_level,
                "experience_years": experience_years,
                "percentage_of_applications": int(percentage_of_applications),
                "technologies_mentioned": detail_data["technologies_mentioned"]
            }

        next_page = (response
                     .css(".pagination .page-item")[-1]
                     .css("::attr(href)").get())

        if next_page != "#":
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def __parse_detailed_vacancy(self, response: Response, vacancy: Selector):
        detailed_url = response.urljoin(vacancy.css(".job-list-item__link::attr(href)").get())
        self.driver.get(detailed_url)

        named_technologies = []

        stated_technologies = [tech.text for tech in self.driver.find_elements(
            By.CSS_SELECTOR, ".job-additional-info--item-text"
        )[1].find_elements(By.CSS_SELECTOR, "span")]

        named_technologies += stated_technologies

        vacancy_text = self.driver.find_element(By.CSS_SELECTOR, ".row-mobile-order-2").text

        for category in TECHNOLOGIES.keys():
            for item_name, item_value in TECHNOLOGIES[category].items():
                for name in item_value:
                    if vacancy_text.find(name) != -1:
                        named_technologies.append(item_name)

        return {
           "technologies_mentioned": list(set(named_technologies))
        }
