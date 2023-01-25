from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

URL = "https://www.olx.ua/d/uk/nedvizhimost/kvartiry/"
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(URL)


def get_data_from_table(key):
    return driver.execute_script(
        """function getTextByKey(key) {
            var divs = document.getElementsByTagName("p");
                var text = "";
                for (var i = 0; i < divs.length; i++) {
                    if (divs[i].innerText.indexOf(key) > -1) {
                        text += divs[i].innerText + " ";
                    }
                }
                return text;
            }
        """
        + f"return getTextByKey('{key}');"
    ).split(": ")[1]


def get_price():
    try:
        return driver.find_element(
            By.XPATH, "//*[@id='root']/div[1]/div[3]/div[3]/div[1]/div[2]/div[3]/h3"
        ).text
    except NoSuchElementException:
        return driver.find_element(
            By.XPATH, "//*[@id='root']/div[1]/div[3]/div[3]/div[1]/div[1]/div[3]/h3"
        ).text


def get_location():
    try:
        return driver.find_element(
            By.XPATH,
            "//*[@id='root']/div[1]/div[3]/div[3]/div[2]/div[2]/div/section/div[2]/img",
        ).get_attribute("alt")
    except NoSuchElementException:
        return ""


def found_links():
    advertisements = driver.find_elements(By.CLASS_NAME, "css-rc5s2u")
    return [
        advertisement.get_attribute("href") for advertisement in advertisements
    ]


def parse(link):
    driver.get(link)
    return {
        "Link": link,
        "Price": get_price(),
        "Floor": get_data_from_table("Поверх:"),
        "Superficiality": get_data_from_table("Поверховість:"),
        "Locality": get_location(),
        "Squere": get_data_from_table("Загальна площа:"),
    }


def parser():
    next_url = driver.find_element(
        By.XPATH, '//*[@id="root"]/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/a'
    ).get_attribute("href")
    data = []
    limit = int(
        driver.find_element(
            By.XPATH,
            "//*[@id='root']/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/li[5]/a",
        ).text
    )
    for _ in range(limit):
        links = found_links()
        for link in links:
            data.append(parse(link))
        driver.get(next_url)
        try:
            next_url = driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/a[2]',
            ).get_attribute("href")
        except NoSuchElementException:
            pass
    return data


def olx_parser():
    return pd.DataFrame(parser())
