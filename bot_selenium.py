# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from urllib.parse import urlparse
import requests
from time import sleep
import random
import utility


class BotSelenium():
    driver = None
    is_debug = True
    origin_code = ""
    log_root_dir = 'log/'
    log_dir = ''

    def __init__(self, dir):
        self.log_root_dir = dir

        u = utility.utility()
        path = self.log_root_dir + u.get_current_time()
        self.log_dir = u.mkdir(path)

    def run_chrome(self, url, isHeadless):
        try:
            if isHeadless :
                options = Options()
                options.add_argument('--headless')
                self.driver = webdriver.Chrome(chrome_options = options)
            else:
                self.driver = webdriver.Chrome()

            self.move_url(url)
            return self.driver
        except Exception as e:
            print(e)
            return None

    def close(self):
        try:
            self.driver.close()
            return True
        except Exception as e:
            print(e)
            return False

    def set_timeout(self, t):
        try:
            self.driver.set_page_load_timeout(t)
            return True
        except Exception as e:
            print(e)
            return False

    def reset(self, url):
        self.action_list = []
        self.move_url(url)

    def current_url(self):
        return self.driver.current_url

    #URLに遷移する
    def move_url(self, url):
        self.driver.get(url)
        self.origin_code = self.get_page_source()
        return self.current_url()
        
    #現在のページでのブラウザログを出力する
    def get_browser_log(self):
        log_list = []
        for entry in self.driver.get_log('browser'):
            log_list.append(entry['message'])
        return log_list

    #アクションリストの長さを返す
    def get_action_list_length(self):
        return len(self.action_list)

    def sleep(self, sec):
        sleep(sec)

    #HTMLソースを取得
    def get_page_source(self):
        return self.driver.page_source

    

    def click(self, action_number):
        try:
            text = self.action_list[action_number].text
            tag = self.action_list[action_number].tag_name
            loc = self.action_list[action_number].location
            if self.is_debug:
                print("click text : %s" % text)
            self.action_list[action_number].click()
            return True, text, tag, loc
        except Exception as e:
            print(e)
            return False, e, None, None

    #origin_page_souceと操作後のpage_sourceが同じか判定する。操作結果判定部分
    def is_change_html_source(self):
        source = self.get_page_source()
        if self.origin_code == source:
            print("Not move error")
            return False
        else:
            return True

    #アクションリストの作成
    def make_action_list(self, start_url):
        self.action_list = []
        self.action_list.extend(self.make_tag_list(start_url, 'a'))
        self.action_list.extend(self.make_tag_list(start_url, 'button'))
        self.action_list.extend(self.make_input_type_list('button'))
        self.action_list.extend(self.make_input_type_list('image'))
        self.action_list.extend(self.make_input_type_list('submit'))
        return self.action_list

    #aタグのリスト作成
    def make_tag_list(self, start_url, tag_name):
        return_list = []
        tmp_list = self.get_tag_element_list(tag_name)

        for element in tmp_list:
            if self.is_add_action_list(element, start_url):
                return_list.append(element)
        
        return return_list

    #inputのtypeによるリスト収集
    def make_input_type_list(self, attribute_name):
        tag_elements_list = []
        temp_list = self.get_tag_element_list('input')
        for element in temp_list:
            t = element.get_attribute("type")
            if t == attribute_name and self.is_element_enable(element):
                tag_elements_list.append(element)
        return tag_elements_list

    #指定タグのリストを集める
    def get_tag_element_list(self, tag_name):
        xpath = '//' + tag_name
        tag_elements_list = self.driver.find_elements_by_xpath(xpath)
        return tag_elements_list
    
    


    #要素がenableか確認
    def is_element_enable(self, element):
        if element == None : return False
        return True if element.is_enabled() and element.is_displayed() else False

    #aタグが自ドメイン内か確認
    def is_element_href_in_domain(self, element, url):
        if element == None : return False
        try:
            href = element.get_attribute("href")
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            return True if domain in href else False
        except Exception as e:
            print(e)
            return False

    #現在のurlがドメイン内か確認
    def is_current_url_in_domain(self, url):
        domain = urlparse(url).netloc
        return True if domain in self.current_url() else False

    #アクションリストに追加判定
    def is_add_action_list(self, element, start_url):
        if element == None : return False
        try:
            if element.tag_name == 'a':
                return True if self.is_element_enable(element) and self.is_element_href_in_domain(element, start_url) else False
            else:
                return True if self.is_element_enable(element) else False
        except Exception as e:
            print(e)
            return False

    #screenshotを取る
    def save_screenshot(self):
        page_width = self.driver.execute_script('return document.body.scrollWidth')
        page_height = self.driver.execute_script('return document.body.scrollHeight')
        self.driver.set_window_size(page_width, page_height)
        path = self.make_file_name_of_screenshot(self.log_dir)
        is_ok = self.driver.save_screenshot(path)
        return is_ok, path


    def make_file_name_of_screenshot(self, dir):
        u = utility.utility()
        word = u.get_last_ward_of_url(self.current_url())
        time = u.get_current_time()
        if dir[-1:] == '/':
            path = dir + word + '_' + time + '.png'
        else:
            path = dir + '/' + word + '_' + time + '.png'
        return path

    #ランダム入力を実行する
    def random_input(self):
        self.random_radio_click()
        self.random_checkbox_click()
        self.random_text_input()
        self.random_email_input()
        self.random_number_input()
        self.random_tel_input()
        

    def send_key_all(self, element_list, text):
        for element in element_list:
            element.send_keys(text)

    def random_element_click(self, element_list):
        length = len(element_list)
        if length > 0:
            try:
                element_list[random.randrange(length)].click()
            except Exception as e:
                print(e)
                
    def random_text_input(self):
        text_list = self.make_input_type_list('text')
        text_list.extend(self.make_input_type_list('password'))
        text_list.extend(self.make_input_type_list('search'))
        self.send_key_all(text_list, "' OR 'a'='a")

    def random_email_input(self):
        text_list = self.make_input_type_list('email')
        self.send_key_all(text_list, "testerchan@testerchan.co.jp")

    def random_number_input(self):
        text_list = self.make_input_type_list('number')
        self.send_key_all(text_list, "0123456789")

    def random_tel_input(self):
        text_list = self.make_input_type_list('tel')
        self.send_key_all(text_list, "090-1234-5678")

    def random_radio_click(self):
        radio_list = self.make_input_type_list('radio')
        self.random_element_click(radio_list)

    def random_checkbox_click(self):
        checkbox_list = self.make_input_type_list('checkbox')
        self.random_element_click(checkbox_list)

    def alert_ok(self):
        try:
            Alert(self.driver).accept()
            return True
        except Exception as e:
            return False
    

