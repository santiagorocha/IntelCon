# !/usr/bin/python3

import time, requests

from bs4 import BeautifulSoup
from stem.connection import connect

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Scraper:
    # Setting proxy configuration to send requests trough Tor network
    # Tor browser must be initialized before running this script
    _PROXY_HOST = "127.0.0.1"
    _PROXY_PORT = 9150
    # If we use the requests library, a header must be setted since this library
    # uses a header by default and it can be easy to block in any web page
    _HEADER = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-language":"es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
                "Connection":"keep-alive"
            }

    def __init__(self):
        """Initializing the a new requests session, firefox driver options and profile
        """
        self.TOR_SESSION = requests.session()
        self.firefox_options = Options()
        self.firefox_profile = webdriver.FirefoxProfile()

    def setPreferences(self):
        """In this function, the preferences are setted, the headless configuration
        can be changed to True if we want to avoid the scraper to open a GUI.
        Preferences are setted to make all GET or POST requests through the Tor Network
        """
        self.firefox_options.headless = False

        self.firefox_profile.set_preference("network.proxy.type", 1)
        self.firefox_profile.set_preference("network.proxy.socks", self._PROXY_HOST)
        self.firefox_profile.set_preference("network.proxy.socks_port", self._PROXY_PORT)

    def extractor(self):
        """This function is in charge of crawl a web page and then scrape from a 
        specific page certain information.
        """
        try:
            self.setPreferences()
            firefox = webdriver.Firefox(options=self.firefox_options, firefox_profile=self.firefox_profile)
            print("[!] Getting post links in Subsections")
            # This will be the starting page for the crawler
            firefox.get("https://example.com/Forum-Tutorials")

            # Explicit wait until an element in the DOM HTML appears, cant be filtered by
            # ID, TAG_NAME, XPATH, ETC...
            if WebDriverWait(firefox, 30).until(EC.presence_of_element_located((By.ID, "id_value"))):

                while True:

                    page_source = firefox.page_source
                    bs_obj = BeautifulSoup(page_source, "html.parser")
                    # This is the HTML element where we can find the link of each item in the list of posts,
                    # depending of how is locate in the DOM, we need to change this according to the forum
                    post_links = bs_obj.find("table", {"class":"tborder clear"}).findAll("tr", {"class":"inline_row"})
                    for post_link in post_links:
                        link = post_link.find("a")
                        if link.attrs["href"] is not None:
                            # Print the link retreived from the HTML DOM, we should evaluate if its an internal or 
                            # external link, and also, if necessary, add the base url of the forum at the beggining.
                            print(link.attrs["href"])

                    try:
                        # Here we find the button to to make a click and go to the next page in the pagination list
                        next_button = firefox.find_element_by_class_name("pagination_next")
                        if next_button:
                            next_button.click()
                            firefox.implicitly_wait(5)
                        else:
                            break
                    except NoSuchElementException:
                        break

            # This is the example web page, will make a GET requests and extract from that page certain information
            firefox.get("https://example.com/Thread-Advance-RAT-Tutorial")

            # Explicit wait until an element in the DOM HTML appears, cant be filtered by
            # ID, TAG_NAME, XPATH, ETC...
            if WebDriverWait(firefox, 20).until(EC.presence_of_element_located((By.ID, "id_value"))):
                page_source = firefox.page_source
                bs_obj = BeautifulSoup(page_source, "html.parser")
                # Locating the post's title HTML element 
                title = bs_obj.find("span", {"class":"x-largetext"}).get_text()
                # Locating the post's content HTML element 
                content = bs_obj.find("div", {"class":"mycode_align"}).get_text()


                print("\n[+] Title of the post is -----> " + title)
                print("\n[+] The content of the post is:")
                print(content)
        except:
            print("[-] Unable to extract from the Forum")

        finally:
            # It's important to always close the web browser instance, if is not closed it's going
            # remain opened in the background
            firefox.close()


    def getTor(self):
        """This function will set the proxy connection for the requests session

        Returns:
            Boolean: Will return True if the proxy connection was succesfully setted
            and False if was any problem
        """
        try:
            self.TOR_SESSION.proxies = {'http': 'socks5://127.0.0.1:9150',
                                        'https': 'socks5://127.0.0.1:9150'}
            return True
        except:
            print("[-] Problem setting a Tor proxy")
            return False

    def checkTor(self):
        """This function will try to connect to the Tor Browser Controller and 
        perform further actions

        Returns:
            Boolean: Will return True the controller succesfully connected to the
            Tor browser controller, otherwise will return False
        """
        controller = connect()
        if not controller:
            print("[-] Tor is not running")
            return False
        else:
            print("[+] Tor is running")
            return True

    def getTorSession(self, getUrl):
        """This functions will make a requests using the requests session which is
        already using the Tor proxy.
        """
        tor = self.getTor()
        try:
            if tor:
                req = self.TOR_SESSION.get(getUrl, headers = self._HEADER)
                # time.sleep(random.randint(15, 20))
                return req
            else:
                print("[-] Not able to get a tor proxy connection")
        except:
            print("[-] Problem getting the url: "+getUrl)
            return None

    def getSessionInfo(self):
        """This function will scrape from the page iplocation.com, the IP used in the connection
        and the country that belongs to that IP
        """
        try:
            url = "https://iplocation.com/"
            req = self.getTorSession(url)
            bs_obj = BeautifulSoup(req.text, "html.parser")
            ip = bs_obj.find("table", {"class":"result-table"}).findAll("tr")[0].find("b",{"class":"ip"}).get_text()
            country = bs_obj.find("table", {"class":"result-table"}).findAll("tr")[3].find("span",{"class":"country_name"}).get_text()
            print("[+] Connected from IP: {} - {}".format(ip, country))
        except: #TypeError as e:
            #print("[-] Couldn't get connection info -> "+str(e))
            pass


def run():

    scrape = Scraper()

    if scrape.checkTor():
        scrape.getSessionInfo()
        scrape.extractor()

if __name__ == "__main__":
    run()