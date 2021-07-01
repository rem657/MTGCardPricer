from selenium import webdriver
import time


class Card:
    def __init__(self, card_name: str, card_set: str):
        self.browser = self.open_web_chrome('https://www.facetofacegames.com/')
        # self.name = card_name
        # self.set = card_set
        self.price_ftf = 0.0
        self.name = ''
        self.set = ''
        self.get_price(card_name, card_set)

    @staticmethod
    def open_web_chrome(url: str) -> webdriver.Chrome:
        """
        This method generates a webdriver chrome objected opened to the given `url` and sets.
        :param url: A string of the url the user wishes to open
        :return: A webdriver object
        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920x1080")
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        return browser

    def search_card(self, name: str, set_name: str):
        """
        This method searches in Face to Face games for a card named `name` of the given set `set_name`.
        :param name: A string for the name of the magic the gathering card
        :param set_name: A string for the name of the set in which the card is printed
        :return:
        """
        if set_name != '':
            search_name = f"{name} - {set_name}"
        else:
            search_name = f"{name}"
        # enter card name
        self.browser.find_element_by_class_name('form-input').send_keys(search_name)
        # press submit button
        self.browser.find_element_by_xpath(
            '/html/body/header/div/div/div[2]/div[1]/div[2]/form/fieldset/div/button').click()

    def get_price(self, name: str, set_name: str):
        """
        This method searches for a given card on the website and returns the highest price for the first product
        :param name: A string for the name of the magic the gathering card
        :param set_name: A string for the name of the set in which the card is printed
        :return: A float for the highest price of the card
        """
        self.search_card(name, set_name)
        time.sleep(1)
        all_product = self.browser.find_elements_by_class_name('product')
        product_1 = all_product[0]
        card_name = product_1.find_element_by_xpath('//article/div[1]/h4/a').text
        card_set = product_1.find_element_by_xpath('//article/div[1]/h4/p').text
        all_price = product_1.find_elements_by_class_name('price-section')
        list_prices = []
        for price in all_price:
            current_price = price.find_elements_by_class_name('price')[0].text
            if current_price[0] == '$':
                list_prices.append(float(current_price[1:]))
            else:
                list_prices.append(float(current_price))
        self.price_ftf = max(list_prices)
        self.name = card_name
        self.set = card_set


if __name__ == '__main__':
    Card('liliana', '')
    # MTGCardPricer('force of will borderless','double master')
