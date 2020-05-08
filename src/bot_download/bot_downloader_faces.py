#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import datetime
import sys
import os
import sys

class Brain:
    def __init__(self, nameset):
        nowtouseonlyonce = datetime.datetime.now()
        self.url = 'https://www.google.com/images'
        self.nb_img_to_dl = 50
        self.nb_alr_dl = 0
        self.page = webdriver.Firefox()
        self.page.get(self.url)

    def close_browser(self):
        self.page.close()

    def sleeping(self, sleep):
        for i in range(sleep):
            time.sleep(1)
            print("Sleeping " + str(i + 1) + " / " + str(sleep) + " seconds\n")

    def search_content(self, to_search):
        searchbox = self.page.find_element_by_class_name("a4bIc")
        searchbox.click()
        search = self.page.find_element_by_xpath('''//*[@id="sbtc"]/div/div[2]/input''')
        search.send_keys(to_search)
        search.send_keys(keys.Keys.RETURN)

    def get_screenshot(self, content):
        k = 0
        for i in range(1, 10):
            for p in range(k, k + 1080):
                self.page.execute_script("window.scrollTo(" + str(k) +", " + str(p) + ");")
                k = p
            self.sleeping(5)
            self.page.save_screenshot(content + "_" + str(i) + ".png")

def help():
    print("\n---BOT_DOWNLOADER---\n\nUSAGE:\tpython3 [bot_file].py [names_file]")
    print("\nDESCRIPTION:\n\tThis file contains a bot that load a name_file")
    print("\tConnect itself on www.google.com/img")
    print("\tAnd takes screenshots to build a dataset of unknown_faces for face_recognition projects")
    print("\tYou may need to install selenium and geckodriver to use it\n")

def bot(name_file):
    fd = open(name_file, 'r')
    nameset = fd.read()
    nameset = nameset.splitlines()
    current_name = nameset[1]
    nb_names = int(nameset[0])
    bot = Brain(nameset)

    for i in range(1, nb_names):
        current_name = nameset[i]
        bot.search_content(current_name)
        bot.get_screenshot(current_name)
        bot.page.get(bot.url)
    fd.close()
    bot.close_browser()

def main():
    if len(sys.argv) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        help()
    else:
        bot(sys.argv[1])
        print("Bot succesfully takes screenshot\n")



if __name__ == "__main__":
    main()