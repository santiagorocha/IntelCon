# Scraping Forums for Cyber Threat Intelligence in IntelCon

This is a mini-tutorial as a result of the talk "Scraping Forums for Cyber Threat Intelligence" by Ginseg on 28 July 2020
In order to properly configure the tool, you should understand the HTML DOM. You can have a good start of this looking at my talk at IntelCon following the next link https://www.youtube.com/channel/UCLH1JjgG6dmbhYYQSzM7-4w.

## Introduction

Online Forums could be an important asset for Cyber Threat Intelligence, but to properly acquire information from these sources is necessary to avoid implemented harvesting countermeasures that can pose a significant challenge such as obfuscation, authentication, honeypots, anti-bots implementations, among others.
Before executing any of the scripts, you need to open a Tor Browser instance since all of the requests made to the forum, will be canalized usnig the default Tor port.

## Scrapy - Web-Crawling Framework

Scrapy is a python Library used to crawl and scrape a web page handling much of the complexity that entails crawling and scraping content from a web page such as finding and evaluating links, crawling domains or lists of domains easily, amont others.

To use scrapy, you should first installing using `pip install scrapy`. After a successful installation, you should go to wikiCTI/wikiCTI/articleSpider.py file and configure Scrapy for your needs. As you can see there is a code ready to use which moves within all internal links in Wikipedia starting from a specific article and extracts the article title in each visit.

If you look inside articleSpider.py, within the class ArticleSpider, you can see the `start_urls` variable which tells the crawler where to start and keep parsing internal hyperlinks to visit, in addition to this, in the `rules` variable we need to define the allowed links to parse using regular expressions. There is also a method named parse_item, which is in charge of extract the information needed from each page using an xpath selector.

To run scrapy you must go back to wikiCTI and execute the next command: `scrapy crawl wikicti`. You can see that all article title are being parsed and showed to you, this is an easy way of scraping a webpage, but there are more approaches that allow to perform a more customized Scrape for Online Forums.

## hiddenInputs.py

One of the used counter-measures by online forums to avoid being harvesting by Scrapers, is to hide fields using CSS features so the value contained in the field will be visible by the browser but invisible to the user simply looking to the page. You can change the source code following the comments depending on which forum you want to analyze.

## captcha.py

This script will import the pytesseract. Pytesseract is an Optical Character Recognition (OCR) Library that will try to recognize and retrieve the text embedded in images. This is a feature that can be added to any Scraper tool since most of the forums use CAPTCHA as an anti-bot countermeasure in the registration or login form. captcha.py is using the image conteined in captcha.jpeg and try to retrieve the text within the image.

## scraper.py

This is a basic Scraper that will parse all section hyperlinks in an online forum. Also will retrieve certain information from a post and show to the user. This is an example of how to crawl and extract valuable information that can be further analyzed to generate CTI assets.

** For more detailed information you can see the pdf attached to this repository which are the slides for my talk **

