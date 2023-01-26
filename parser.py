from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

URL = "https://www.olx.ua/d/uk/nedvizhimost/kvartiry/"
driver = webdriver.Chrome()
driver.get(URL)


def get_data_from_table(key: str) -> str:
    """
    This function takes a string parameter "key" and returns a string.
    It uses the Selenium webdriver's execute_script method to execute a JavaScript
    function that finds all the "p" tags on the page and checks if each one contains the
    key parameter. If it does, it adds the text of that "p" tag to a variable called "text".
    The function then returns the "text" variable.

    :param key: key word which parser search on advertisement page
    :return: function returns data of key word
    """
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


def get_price() -> str:
    """
    This function search and return the price from advertisement page

    :return: function returns price
    """
    try:
        return driver.find_element(
            By.XPATH, "//*[@id='root']/div[1]/div[3]/div[3]/div[1]/div[2]/div[3]/h3"
        ).text
    except NoSuchElementException:
        return driver.find_element(
            By.XPATH, "//*[@id='root']/div[1]/div[3]/div[3]/div[1]/div[1]/div[3]/h3"
        ).text


def get_location() -> str:
    """
    This function search and return the locality from advertisement page

    :return: function returns locality
    """
    try:
        return driver.find_element(
            By.XPATH,
            "//*[@id='root']/div[1]/div[3]/div[3]/div[2]/div[2]/div/section/div[2]/img",
        ).get_attribute("alt")
    except NoSuchElementException:
        return ""


def found_links() -> list[str]:
    """
    This function search all advertisements on list page

    :return: function return list of links on advertisements
    """
    advertisements = driver.find_elements(By.CLASS_NAME, "css-rc5s2u")
    return [
        advertisement.get_attribute("href") for advertisement in advertisements
    ]


def parse(link: str) -> dict:
    """
    This function takes a string parameter "link" and returns a dictionary.
    It uses the Selenium webdriver's get method to navigate to the link passed
    as an argument. Then it uses the get_price, get_data_from_table, and get_location
    functions to extract the price, floor, superficiality, locality, and square
    footage of the advertisement. It then returns a dictionary with the extracted
    data, where the keys are the names of the data elements and the values are the
    extracted values.

    :param link: link on advertisement page
    :return: dict of data
    """
    driver.get(link)
    return {
        "Link": link,
        "Price": get_price(),
        "Floor": get_data_from_table("Поверх:"),
        "Superficiality": get_data_from_table("Поверховість:"),
        "Locality": get_location(),
        "Square": get_data_from_table("Загальна площа:"),
    }


def parser() -> list[dict]:
    """
    This function returns a list of dictionaries. It first uses the Selenium
    webdriver's find_element method to find the link to the next page of the
    website. It initializes an empty list called "data" and a variable "limit"
    that is the total number of pages to scrape. It then uses a for loop to traverse
    through each page by calling the found_links and parse functions to extract the
    data and adding it to the "data" list. It returns the "data" list.

    :return: function returns list of dictionaries with data
    """
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
    """
    :return: function returns a Pandas DataFrame.
    """
    return pd.DataFrame(parser())
