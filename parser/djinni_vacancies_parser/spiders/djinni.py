import scrapy
from scrapy.http import Response

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

            if english_level not in ENGLISH_LEVELS_DJINNI:
                english_level = "Not stated"

            experience_years = (EXPERIENCE_YEARS_DJINNI
                                .get(experience_years, "Not stated"))

            yield {
                "vacancy_name": (vacancy.css(".job-list-item__link::text")
                                 .get()
                                 .strip()),
                "location_text": (vacancy.css(".location-text::text")
                                  .get()
                                  .strip()
                                  .replace("\t", "")
                                  .replace("\n", "")),
                "english_level": english_level,
                "experience_years": experience_years,
            }

        next_page = (response
                     .css(".pagination .page-item")[-1]
                     .css("::attr(href)").get())

        if next_page != "#":
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
