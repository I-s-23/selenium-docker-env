# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display


class Chrome:
    def preparation(self, headless: bool, set_size=(0, 0)):
        """SeleniumのChromeWebDruverの準備

        Args:
            headless (bool): ヘッドレスでブラウザ起動を行う場合True

        Returns:
            [type]: 必要な設定の入ったChromeのWebDriverを返却
        """

        display = (
            Display(visible=True, size=(800, 600))
            if headless == True
            else Display(
                visible=True,
                size=(1920, 2080) if set_size == (0, 0) else set_size,
                backend="xvfb",
                use_xauth=True,
            )
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

    def open_run_task(self, function, headless: bool, args1=None):
        """ブラウザの自動操作。引数の関数を実行。エラーハンドリングなど"""

        driver, display = self.preparation(headless)

        try:
            function(driver) if args1 is None else function(driver, args1)

        except TimeoutException:
            print("Timeout Error", sys.exc_info()[0])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            driver.close()
            driver.quit()
            display.stop()
