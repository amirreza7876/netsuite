from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from termcolor import colored
import time
import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-u', help='username')
parser.add_argument('-p', help='password')
args = parser.parse_args()


def logger(title, desc, color=None):
    time = datetime.datetime.now()
    msg ='{0} {1}\t{2}'.format(
        (str(time.hour)
        +":"
        +str(time.minute)
        +":"
        +str(time.second)),
        title,
        desc)
    print(colored(msg, color))


class console_type():
    INFO = 'yellow'
    ERROR = 'red'
    SUCCESS = 'green'


class NetSuite():

    def __init__(self,u,p):
        self.u = u
        self.p = p
        self.base_url = "http://user.qiau.ac.ir/web/"
        self.secend_url = "http://user.qiau.ac.ir/web/netsuite.cgi"
        self.start()


    def start(self):
        self.driver_init()
        self.getToUrl(self.base_url)
        self.login()
        self.getToUrl(self.secend_url)
        time.sleep(5)
        self.discnnect()
        self.close_driver()


    def driver_init(self):
        options = Options()
        options.headless = True
        binary = FirefoxBinary('/usr/bin/firefox')
        self.driver = webdriver.Firefox(options=options, firefox_binary=binary)
        logger("selenium", "driver initialized", console_type.SUCCESS)


    def getToUrl(self,url):
        self.driver.get(url)
        logger("selenium", "get to: "+url, console_type.INFO)


    def login(self):
        username = self.driver.find_element_by_name("uid")
        username.clear()
        username.send_keys(args.u)
        passw = self.driver.find_element_by_name("pwd")
        passw.clear()
        passw.send_keys(args.p)
        loginbtn = self.driver.find_element_by_xpath("//input[@value='Login'][@type='submit']")
        loginbtn.click()
        logger("selenium", "trying login to "+self.u, console_type.INFO)
        

    def discnnect(self):
        try:
            dicsbtn = self.driver.find_element_by_id("ext-gen72")
            dicsbtn.click()
            logger("selenium", "trying to disconnect", console_type.INFO)
        except NoSuchElementException as e:
            logger("selenium", "user or pass incorrect", console_type.ERROR)


    def close_driver(self):
        logger("selenium", "driver closed :)", console_type.SUCCESS)
        self.driver.close()


if __name__ == '__main__':
    net = NetSuite(args.u,args.p)
