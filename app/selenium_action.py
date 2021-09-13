# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from time import sleep
import enum
import os
import sys
import datetime
from typing import no_type_check
import pyautogui
import Xlib.display


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class Context(enum.Enum):
    xpath = enum.auto()
    css_selector = enum.auto()
    id = enum.auto()
    image = enum.auto()
    _class = enum.auto()


@dataclass
class Element:
    """XpathやCSS_Selecorなどの各要素の属性と値"""

    value: str
    context: int


@dataclass
class LogingInformation:
    url: str
    input_element: list[str]
    input_value: list[str]
    click_element: str


class Page:
    def change(self, driver: webdriver.Chrome, url: str | list[str], time=3):
        """URLのページにChromeで移動。画面が表示されるまで待機

        Args:
            driver ([type]): Chromeを表示するためのWebDriver
            wait ([type]): 待機時間など
            url (str): 繊維先URL
        """

        self.change_wait(driver, url, time) if type(url) is str else [
            self.change_wait(driver, x, time) for x in url
        ]

    def change_wait(self, driver: webdriver.Chrome, url: str, time=3):
        """URLのページにChromeで移動。画面が表示されるまで待機

        Args:
            driver ([type]): Chromeを表示するためのWebDriver
            wait ([type]): 待機時間など
            url (str): 繊維先URL
        """

        driver.get(url)
        WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located)
        sleep(time)

    def change_click(
        self,
        driver: webdriver.Chrome,
        urls: list[str],
        elements: list[Element | list[Element]],
        sleep_time: float = 0,
    ):
        """WebPage遷移＆XpathClickをする作業、Xpathは複数でも対応 ここの待機処理が機能していない可能性あり

        Args:
            driver ([type]): [description]
            wait ([type]): [description]
            urls (list[str]): [description]
            elements (list[str]): [description]
        """
        for url, element in zip(urls, elements):
            try:
                self.change(driver, url)
                self.clicks(driver, element) if type(element) is list else self.click(
                    driver, element
                )
                sleep(sleep_time)
            except:
                print(
                    "Unexpected error:",
                    sys.exc_info()[0],
                    driver.title,
                    driver.current_url,
                )


    def clicks(self, driver: webdriver.Chrome, elements: list[Element], wait = 1):

        for element in elements:
            self.click(driver, element, wait)


    def scrol_down(
        self, driver: webdriver.Chrome, url: str = "", page_end: bool = False, wait: int = 0
    ):
        """WebページのUrlを入れればそこに遷移後スクロールを行う

        Args:
            driver (webdriver.Chrome): [description]
            element (Element): [description]
            url (str, optional): [description]. Defaults to "".
        """

        if url != "":
            self.change(driver, url, wait)
        elem = driver.find_element_by_tag_name("html")
        elem.send_keys(Keys.END) if page_end else elem.send_keys(Keys.PAGE_DOWN)
        sleep(2)

    def reload(self, driver: webdriver.Chrome, url: str = "", wait: int = 0):
        """WebページのUrlを入れればそこに遷移後ページのリロードを行う

        Args:
            driver (webdriver.Chrome): [description]
            url (str, optional): [description]. Defaults to "".
        """

        if url != "":
            self.change(driver, url, wait)
        driver.find_element_by_tag_name("html").send_keys(Keys.F5)
        sleep(wait)

    def image_search(self, pyautogui, target_image: str):

        for _ in range(10):
            position = pyautogui.locateCenterOnScreen(
                os.getenv("IMAGE_DIRECTORY", "") + target_image, grayscale=True, confidence=0.700
            )
            if position is not None:
                return position
            else:
                sleep(1)
        return None

    def image_click(self, target_image: str):
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.getenv("DISPLAY"))
        position = self.image_search(pyautogui, target_image)
        if position is not None:
            pyautogui.click(position)
            print("image click successed")
        return position

    def find_element(self, driver, element: Element):
        try:
            if element.context == Context.xpath.value:
                return driver.find_element_by_xpath(element.value)
            if element.context == Context.css_selector.value:
                return driver.find_element_by_css_selector(element.value)
            if element.context == Context.id.value:
                return driver.find_elements_by_id(element.value)
            if element.context == Context.image.value:
                pyautogui._pyautogui_x11._display = Xlib.display.Display(os.getenv("DISPLAY"))
                return (
                    element if self.image_search(pyautogui, element.value) is not None else False
                )
            if element.context == Context._class.value:
                return driver.find_elements_by_class_name(element.value)

        except:
            return False

    def context_function(self, context: int):
        """属性に応じた処理を返す 要素が有効になるまで待機 + 要素を押下

        Args:
            context: (int): Seleniumボタン要素の属性

        Returns:
            [type]: [description]
        """

        if context == Context.xpath.value:
            return [
                lambda driver, value: WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, value))
                ),
                lambda driver, value: driver.find_element_by_xpath(value).click(),
            ]
        if context == Context.css_selector.value:
            return [
                lambda driver, value: WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, value))
                ),
                lambda driver, value: driver.find_element_by_css_selector(value).click(),
            ]
        if context == Context.id.value:
            return [
                lambda driver, value: WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, value))
                ),
                lambda driver, value: driver.find_element_by_id(value).click(),
            ]
        if context == Context.image.value:
            return [
                lambda _, value: self.image_click(value),
            ]
        if context == Context._class.value:
            return [
                lambda driver, value: WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, value))
                ),
                lambda driver, value: driver.find_elements_by_class_name(value).click(),
            ]


    def click(self, driver: webdriver.Chrome, element: Element, wait = 1):
        """Seleniumで押下処理に待機時間とエラーハンドリングを追加

        Args:
            driver (webdriver.Chrome): [description]
            element (Element): [description]
        """

        click_action = self.context_function(element.context)
        self.selenium_click(driver, element.value, click_action,wait)

    def selenium_click(self, driver: webdriver.Chrome, click_target: str, functions, wait = 1):
        try:
            for func in functions:
                func(driver, click_target)
            sleep(wait)
        except:
            print(
                f"{datetime.datetime.now()} Unexpected error:",
                sys.exc_info()[0],
                driver.title,
                driver.current_url,
                click_target,
            )
            driver.save_screenshot(f"./error/{datetime.datetime.now()}.png")

    def find_element_branch_button(
        self,
        driver,
        target_button: selenium_action.Element  | list[selenium_action.Element],
        cannot_find_button: selenium_action.Element = None,
        message: str = "",
        url: str = "",
    ) -> selenium_action.Element | bool:
        """できればTypeGuirdを実装したい

        Returns:
            [type]: [description]
        """

        if url:
            page.change(driver, url)
        if type(target_button) == list:
            for t in target_button:
                target = t if page.find_element(driver, t) else False
                if target:
                    return target
            print(f"not {message}")
            print("list")
            return False
        else:
            target = target_button if page.find_element(driver, target_button) else cannot_find_button
            if target is None:
                print(f"not {message}")
                print("str")
                return False
            return target


    def find_and_find_element(self, driver,target_button: selenium_action.Element):
        try:
            if page.find_element(driver, target_button):
                page.click(driver,target_button)
                return self.find_and_find_element(driver,target_button)
        except:
            return
