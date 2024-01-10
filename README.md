# Top technologies to learn based on Djinni vacancies

## How to update(scrape) data

1) Clone repository

    `git clone https://github.com/mykolamateichuk/top-technologies-to-learn-based-on-djinni`


2) Go to the cloned folder
    
    `cd top-technologies-to-learn-based-on-djinni`


3) Go to the parser folder

    `cd parser`


4) Scrape data using Scrapy

    `scrapy crawl djinni -O vacancies.csv`

5) Now your data is up-to-date so you can just rerun jupyter notebook in folder `analysis`


## Analysis

As of `09.01.2024` there are 198 Python vacancies on djinni, after analysing 
each of them I was able to build a histogram of top 20 popular technologies that 
were mentioned in those vacancies(either tagged or mentioned in text).

![output.png](..%2F..%2F..%2FDesktop%2Foutput.png)

As you can see the most popular technologies were `HTTP`, `Python`, `SQL`, `Docker` and `Git`.
And it is not surprising, because Python nowadays mostly used either for web-dev or for data science 
purposes and knowing technologies such as HTTP, SQL and Docker is crucial for those fields.

Also we can see some not Python related technologies in the list, such as: `JavaScript`, `ReactJS` and `HTML`.
Those technologies are also important to know for productive web-development.

Next chart was build to prove that you should have a high level of English to have
a bigger chance of securing a job.

![output1.png](..%2F..%2F..%2FDesktop%2Foutput1.png)

As you can see, almost `60%` of job vacancies ask for Upper-Intermediate level of english,
and other `20%` for Intermediate. It's also interesting to see that Advanced/Fluent level of english
is not really needed today, because only `4.5%` of vacancies stated it as a requirement.

Next chart shows the percentages of vacancies for a specific years of experience needed to get the job.

![output2.png](..%2F..%2F..%2FDesktop%2Foutput2.png)

This chart shows that nowadays there are more vacancies for experienced developers,
than for juniors or trainees. In my opinion this is strongly connected to the ongoing War in Ukraine.
A lot of the companies do not want to expend their teams or start new projects because of it,
so there are less junior developers needed.