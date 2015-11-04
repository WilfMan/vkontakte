# -*- coding: utf-8 -*-
from selenium import webdriver
import os
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time


__author__ = 'wilfman'


def _chrome():
    print 'start driver'
    chromedriver = "/home/wilfman/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    print 'ok'
    return driver

def find_e_by_txt(driver, text):
    try:
        e = driver.find_elements_by_(text)
    except:
        pass

def process():
    driver = _chrome()

    driver.get('http://vk.com')
    driver.find_element(by='id', value='quick_email').send_keys('')

    e = driver.find_element(by='id', value='quick_pass')
    e.send_keys('')
    e.submit()

    driver.find_element_by_partial_link_text('Мои Аудиозаписи').click()


    WebDriverWait(driver, 15).until(lambda driver_: driver_.title.lower().startswith(u'аудиозаписи'))
    driver.find_element_by_xpath('//*[@id="audios_albums"]/div[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="album52896548"]/div[1]').click()
    driver.execute_script("""
    scroll = function (){window.scrollTo(0, document.body.scrollHeight);};
    search = function (text){
    var aTags = document.getElementsByTagName("a");
    var searchText = "Earthless";
    var found = null;

    for (var i = 0; i < aTags.length; i++) {
      if (aTags[i].textContent == text) {
        found = aTags[i];
        break;
      }
    }
    return found
    }

    var check = function(){
        if(!search('Earthless')){
            console.log('scroll');
            scroll();
            setTimeout(check, 100);
        }else{scroll();}

    };

    check();
    """)

    time.sleep(20)

    print 1
    html_text = driver.page_source
    driver.close()
    return html_text

if __name__ == '__main__':
    process()
