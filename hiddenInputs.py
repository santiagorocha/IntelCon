from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


INPUTS = {}
HIDDEN_INPUT = {}
# Host IP
PROXY_HOST = "127.0.0.1"
# IP opened by Tor Browser by default
PROXY_PORT = 9150

options = Options()
# If setted to True, Firefox will work without GUI
options.headless = False

# Setting proxy configuration to filter all requests through Tor Network
# Tor browser must be initialized before running this script
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 9150)

firefox = webdriver.Firefox(options=options, firefox_profile=profile)

def autVerif():
    """This function retrieves both shown inputs and hidden inputs
    from a Login Form in any web page using functions is_displayed()
    """
    try:
        firefox.get("www.example.com/login") # Url where the login is located

        # Explicit wait until an element in the DOM HTML appears, cant be filtered by
        # ID, TAG_NAME, XPATH, ETC...
        if WebDriverWait(firefox, 30).until(EC.presence_of_element_located((By.ID, "id_value"))):

            fields = firefox.find_elements_by_tag_name("input")
            print("[!] Obtaining inputs in Login Form")
            for field in fields:
                if not field.is_displayed():
                    HIDDEN_INPUT[field.get_attribute("name")] = field.get_attribute("value")
                elif field.is_displayed():
                    INPUTS[field.get_attribute("name")] = field.get_attribute("value")

    except:
        print("[-] Problem getting Inputs")

    finally:
        print("[+] Input fields in login page: ")
        print(INPUTS)
        print("\n[+] Hidden Input fields in login page: ")
        print(HIDDEN_INPUT)
        firefox.close()

def hiddenVerif():
    """This function will try to retrieve all links that are hidden
    and cannot be seen by a human navigating within a web page. This will
    help us to identify potential honeypots for the scraper in any web page.
    """
    try:
        print("[!] Getting possible honeypots")
        firefox.get("www.webtocatchhoneypots.com")

        # Explicit wait until an element in the DOM HTML appears, cant be filtered by
        # ID, TAG_NAME, XPATH, ETC...
        if WebDriverWait(firefox, 30).until(EC.presence_of_element_located((By.ID, "id_value"))):
            links = firefox.find_elements_by_tag_name("a")
            print("[+] Possible honeypot links: ")
            for link in links:
                if not link.is_displayed():
                    if link.get_attribute("href") is not None:
                        print(link.get_attribute("href"))

    except:
        print("[-] Problem getting Inputs")

    finally:
        # It's important to always close the web browser instance, if is not closed it's going
        # remain opened in the background
        firefox.close()