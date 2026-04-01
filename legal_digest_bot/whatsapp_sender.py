"""Send generated PDF to WhatsApp Web group using Selenium."""

from __future__ import annotations

from pathlib import Path

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WhatsAppSender:
    def __init__(self, profile_dir: str = ""):
        options = ChromeOptions()
        if profile_dir:
            options.add_argument(f"--user-data-dir={profile_dir}")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 40)

    def send_pdf_to_group(self, group_name: str, file_path: Path) -> None:
        self.driver.get("https://web.whatsapp.com/")

        search_box = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        )
        search_box.click()
        search_box.send_keys(group_name)

        group = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//span[@title='{group_name}']"))
        )
        group.click()

        attach_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus']"))
        )
        attach_btn.click()

        file_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys(str(file_path.resolve()))

        send_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        )
        send_btn.click()

    def close(self) -> None:
        self.driver.quit()
