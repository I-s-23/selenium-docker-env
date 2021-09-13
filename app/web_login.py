# -*- coding: utf-8 -*-
from __future__ import annotations

from time import sleep
import os
import sys
from dataclasses import dataclass, field

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

import selenium_action
import datetime


@dataclass
class Url:
    targrt_page: str = os.getenv("TARGRT_PAGE", "")


class Login:
    def used_login_information(self):
        login = {
            "dmm": selenium_action.LogingInformation(
                "https://accounts.dmm.com/service/login/password/",
                ["login_id", "password"],
                [os.getenv("TEST_USERNAME", ""), os.getenv("TEST_PASSWORD", "")],
                "//form[@name='loginForm']//input[@type='submit']",
            )
        }

        return login

    def browser_preparation(self, headless: bool):
        """SeleniumのChromeWebDruverの準備

        Args:
            headless (bool): ヘッドレスでブラウザ起動を行う場合True

        Returns:
            [type]: 必要な設定の入ったChromeのWebDriverを返却
        """

        display = (
            Display(visible=True, size=(800, 600))
            if headless == True
            else Display(visible=True, size=(1920, 1080), backend="xvfb", use_xauth=True)
        )
        display.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless") if headless == True else options.add_argument(
            "--window-size=1920x1080"
        )
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # <=これを追加
        options.add_argument("--disable-gpu")  # ヘッドレスモードで起動するときに必要
        options.add_argument("--lang=ja-JP")
        options.add_experimental_option(
            "prefs",
            {
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )

        # ブラウザを開く（pathは、webdriverをインストールした場所に設定してください。）
        return webdriver.Chrome(ChromeDriverManager().install(), options=options), display

    def browser_open_run_task(self, function):
        """ブラウザの自動操作。引数の関数を実行。エラーハンドリングなど"""

        driver, display = self.browser_preparation(False)

        try:
            function(driver)

        except TimeoutException:
            print("Timeout Error", sys.exc_info()[0])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            driver.close()
            driver.quit()
            display.stop()

    def login_page(
        self,
        driver: webdriver.Chrome,
        login_used_information: selenium_action.LogingInformation,
        change_url: bool = True,
    ):
        """ログイン処理 IDとパスワードをクリックするページに関して必要情報で各サイトで使い回し可能
        Args:
            driver ([type]): [description]
            login_used_information (): [description]
        """

        if change_url:
            driver.get(login_used_information.url)
        for element, value in zip(
            login_used_information.input_element, login_used_information.input_value
        ):
            id = driver.find_element_by_id(element)
            id.send_keys(value)
        driver.find_element_by_xpath(login_used_information.click_element).click()
        sleep(2)
