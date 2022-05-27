import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    JavascriptException,
    NoSuchElementException
)

import requests
import time
import tkinter as tk

from requests.exceptions import ConnectionError

from threading import Thread


bet2 = ''
bet3 = ''
bet4 = ''
bet5 = ''

flag = 0


class MainApp:

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('400x200')

        self.link_field = tk.Text(width=40, height=3)
        self.link_field.grid(row=0, column=0, padx=10, pady=10)

        self.login_field = tk.Entry(width=40)
        self.login_field.grid(row=1, column=0, sticky='w', padx=30)

        self.pass_field = tk.Entry(width=40)
        self.pass_field.grid(row=2, column=0, sticky='w', padx=30, pady=3)

        button_auth = tk.Button(text='Login', height=1,
                                width=6, command=self.open_url)
        button_auth.grid(row=3, column=0, padx=30, pady=10, sticky='w')

        make_windows = tk.Button(text='Tabs', height=1,
                                 width=6, command=load_windows)
        make_windows.grid(row=3, column=0, padx=100, pady=30, sticky='w')

        make_bets_button = tk.Button(text='Make bets', height=1,
                                     width=8, command=make_bets)
        make_bets_button.grid(row=3, column=0, padx=160, pady=30, sticky='w')


    def open_url(self):
        link = self.link_field.get("1.0", "end")
        login = self.login_field.get()
        password = self.pass_field.get()

        driver.execute_script(f'window.open("{link[:-2]}")')
        driver.switch_to.window(driver.window_handles[-1])

        tab_state = driver.execute_script('return document.readyState')


        try:
            auth_button = driver.find_element(By.XPATH, '//*[@id="curLoginForm"]/span')
            auth_button.click()

            login_form = driver.find_element(By.XPATH, '//*[@id="auth_id_email"]')
            login_form.send_keys('')  # write your login

            pass_form = driver.find_element(By.XPATH, '//*[@id="auth-form-password"]')
            pass_form.send_keys('')  # write your pass

            entry_button = driver.find_element(By.XPATH, '//*[@id="loginout"]/div[2]/div/div/form/button/span')
            entry_button.click()

        except NoSuchElementException:
            pass

        except ElementClickInterceptedException:
            pass


class HelpThread(Thread):
    def __init__(self, link):
        Thread.__init__(self)
        self.link = link

    def run(self):
        driver.execute_script(f'window.open("{self.link}")')

    def stop(self):
        self._is_running = False


def save_bet_button(bet_link):
    for x in range(2, len(driver.window_handles)):
        driver.switch_to.window(driver.window_handles[x])
        bet = driver.find_element(By.CSS_SELECTOR, '#sports_right > div > div:nth-child(2) > div > div.c-tabs__'
                                                   'content > div.coupon__content > div > div.coupon__settings > '
                                                   'div.grid.coupon-btn-group.u-npv > div > div > div > button')
        bet_link = bet

        if driver.window_handles == 6:
            break


def close_tabs():
    try:
        while True:
            if len(driver.window_handles) == 2:
                break

            driver.switch_to.window(driver.window_handles[2])
            driver.execute_script('window.close()')

    except IndexError:
        pass


def webdriver_version(version):
    if version == 'usually':
        driver = webdriver.Chrome()

        return driver

    elif version == 'antidetect':
        opts = uc.ChromeOptions()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
        driver = webdriver.Chrome(options=opts)

        return driver


def load_windows():
    driver.switch_to.window(driver.window_handles[-1])
    link = driver.current_url

    while True:
        if len(driver.window_handles) == 6:
            break

        thread1 = HelpThread(link=link)
        thread1.start()
        thread1.join()
        thread1.stop()

    save_bet_button(bet2)
    save_bet_button(bet3)
    save_bet_button(bet4)
    save_bet_button(bet5)


def make_bets():
    for x in range(1, len(driver.window_handles)):
        y = len(driver.window_handles) - 1
        
        try:
            driver.switch_to.window(driver.window_handles[x])

            place_a_bet_button = driver.execute_script('return document.querySelector("#sports_right > div > div:'
                                                       'nth-child(2) > div > div.c-tabs__content > div.coupon__'
                                                       'content > div > div.coupon__settings > div.grid.coupon-btn-'
                                                       'group.u-npv > div > div > div > button")')

            place_a_bet_button.click()


            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()
            tr_actions = driver.execute_script(f'return document.querySelector("body > discards-main").shadowRoot.'
                                               f'querySelector("iron-pages > discards-tab").shadowRoot.querySelector'
                                               f'("#tab-discards-info-table-body > tr:nth-child({y}) > td.actions-cell'
                                               f' > div:nth-child(2)")')
            tr_actions.click()
            tr_actions.click()
            tr_actions.click()

        except AttributeError:
            break

        except ElementClickInterceptedException:
            ActionChains(driver).move_by_offset(3, 3).click().perform()

            place_a_bet_button = driver.execute_script('return document.querySelector("#sports_right > div > div:'
                                                       'nth-child(2) > div > div.c-tabs__content > div.coupon__'
                                                       'content > div > div.coupon__settings > div.grid.coupon-btn-'
                                                       'group.u-npv > div > div > div > button")')

            place_a_bet_button.click()


            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()
            tr_actions = driver.execute_script(f'return document.querySelector("body > discards-main").shadowRoot.'
                                               f'querySelector("iron-pages > discards-tab").shadowRoot.querySelector'
                                               f'("#tab-discards-info-table-body > tr:nth-child({y}) > td.actions-cell'
                                               f' > div:nth-child(2)")')
            tr_actions.click()
            tr_actions.click()
            tr_actions.click()

        except IndexError:
            pass


def auth_key():
    try:
        response = requests.post('http://127.0.0.1:5000/auth', json={'key': key_field.get("1.0", "end")})
        if response.json()['status'] == 'Ok':
            start_window.destroy()
            global flag
            flag = 1

    except ConnectionError:
        pass


start_window = tk.Tk()
start_window.geometry('350x130')

key_field = tk.Text(width=40, height=2)
key_field.grid(row=0, column=0, padx=10, pady=10)

button_auth1 = tk.Button(text='Auth', height=1,
                         width=6, command=auth_key)
button_auth1.grid(row=2, column=0, padx=10, pady=30, sticky='w')

start_window.mainloop()


if flag == 1:
    driver = webdriver_version('usually')
    driver.get('chrome://discards')

    app = MainApp()
    app.window.mainloop()

