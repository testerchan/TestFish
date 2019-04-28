from selenium import webdriver
import requests
from time import sleep

class check_url_http_status():
    checked_url = []

    def check_url_http_status(self, element_list, wait_time):
        error_list = []
        text = ''
        for element in element_list:
            if element.tag_name == "a":
                href = element.get_attribute("href")
                if href != "" and href not in self.checked_url:
                    self.checked_url.append(href)
                    r = requests.get(href)
                    if r.status_code >= 400 :
                        error_list.append(
                            {"code":r.status_code, "url":href}
                        )
                        text += str(r.status_code) + " : " + href + '\n'
                    print(str(r.status_code) + " : " + href)
                    self.sleep(wait_time)
        return text

    def sleep(self, sec):
        sleep(sec)