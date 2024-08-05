from decimal import Decimal
from typing import Dict, List
from time import sleep
from logging import Logger
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import utils


class Site1:
    url = "https://www.lojarelvaverde.com.br/bebida-de-castanha-de-caju-sabor-leite-sem-leite-possible-1l-p3123"

    selectors = {
        "reject_cookie_tab": "body > div.adopt-c-BhSUe",
        "reject_cookie_button": "#adopt-reject-all-button",
        "price_label": "#product-details > b > div > div.procuct-detail > div.product-values > div > div.price > b",
        "buy_button": "#product-details > b > div > div.procuct-detail > b > div.botao_comprar > div > a > button",
        "cart_tab": "#side-cart",
        "cart_qnt_input": "#cart-items > #item-3123 * input",
        "also_bought_tab": "#fancybox-container-1 > div.fancybox-inner > div.fancybox-stage > div > div",
        "also_bought_check_cart_button": ".fancybox-content > .popup-product-added * div.actions.flex > button.w-100.btn-primary.btn.cart",
        "open_cart_button": ".sidecart-button",
        "postcode_input": "#cep",
        "postcode_search_button": "#btn-calc-frete > i > svg > path",
        "shipping_price_labels": "#side-cart > div.cart-total.flex > div.shopping-cart-shipping.flex.w-100 > dl > dl.shipping-options > .option > * > .price",
        "side_cart": "#side-cart",
    }

    def __init__(self, browser: ChromeDriver, logger: Logger) -> None:
        self.browser: ChromeDriver = browser
        self.logger: Logger = logger

    def log(self, *args) -> None:
        if len(args) == 1:
            self.logger.info(args[0])
        else:
            self.logger.info(f"[{args[0]}]{args[1]}")

    def find_element(self, key: str, timeout: float = 2) -> WebElement:
        self.log(key, "searching element...")
        element = WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors[key]))
        )
        self.log(key, "found element.")
        return element

    def find_elements(self, key: str, timeout: float = 2) -> List[WebElement]:
        self.log(key, "searching elements...")
        elements = WebDriverWait(self.browser, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.selectors[key]))
        )
        self.log(key, "found elements.")
        return elements

    def try_press(self, key: str) -> bool:
        try:
            button = self.find_element(key)
            button.click()
            self.log(key, "pressed.")
            return True
        except Exception as e:
            self.log(key, f"not pressed, reason: {type(e)}.")
            return False

    # region COOKIES
    def is_reject_cookies_tab_open(self) -> bool:
        key = "reject_cookie_tab"
        try:
            element = self.find_element(key, 5)
            self.log(
                key,
                f"is{'' if element.is_displayed() else ' not'} opened.",
            )
            return element.is_displayed()
        except Exception as e:
            self.log(key, f"is not opened, reason: {type(e)}.")
            return False

    def press_reject_cookies(self) -> None:
        for _ in range(4):
            if self.try_press("reject_cookie_button"):
                return
            sleep(0.5)

    def wait_reject_cookies_bar_close(self) -> None:
        key = "reject_cookie_tab"
        self.log(key, "waiting to close...")
        WebDriverWait(self.browser, 5).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors[key]))
        )
        self.log(key, "closed.")

    # endregion COOKIES
    # region FRONT
    def get_buy_unit_price(self) -> Decimal:
        key = "price_label"
        element = self.find_element(key)
        self.log(key, f"got unit price for {element.text}.")
        return Decimal(utils.convert_BR_money_to_decimal(element.text))

    def press_buy(self) -> None:
        for _ in range(4):
            if self.try_press("buy_button"):
                return
            sleep(0.5)
        raise Exception("expected to be clicked to continue!")

    # endregion FRONT
    # region ALSO_BOUGHT
    def wait_also_bought_tab_open(self) -> None:
        key = "also_bought_tab"
        self.log(key, "waiting to open...")
        WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.selectors[key]))
        )
        self.log(key, "opened.")

    def press_check_cart(self) -> None:
        for _ in range(4):
            if self.try_press("also_bought_check_cart_button"):
                return
            sleep(0.5)
        raise Exception("expected to be clicked to continue!")

    def wait_also_bought_tab_close(self) -> None:
        key = "also_bought_tab"
        self.log(key, "waiting to close")
        WebDriverWait(self.browser, 10).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors[key]))
        )
        self.log(key, "closed")

    # endregion ALSO_BOUGHT
    # region CART_TAB
    def is_tab_supposed_to_be_open(self) -> bool:
        key = "cart_tab"
        element = self.find_element(key)
        html_class = element.get_attribute("class")
        return html_class is not None and "show-cart" in html_class

    def wait_cart_tab_open(self) -> None:
        key = "cart_tab"
        self.log(key, "waiting to open...")
        element = self.find_element(key)
        d = element.value_of_css_property("transition-duration")
        s = utils.convert_text_seconds_to_float(d)
        sleep(s + 0.1)
        assert self.is_tab_supposed_to_be_open(), "tab is not opened."
        self.log(key, "opened.")

    def wait_cart_tab_close(self) -> None:
        key = "cart_tab"
        self.log(key, "waiting to close...")
        element = self.find_element(key)
        d = element.value_of_css_property("transition-duration")
        s = utils.convert_text_seconds_to_float(d)
        sleep(s + 0.1)
        assert not self.is_tab_supposed_to_be_open(), "tab is not closed."
        self.log(key, "closed.")

    def press_open_cart(self) -> None:
        for _ in range(20):  # try many times
            if self.try_press("open_cart_button"):
                return
            sleep(0.5)
        raise Exception("expected to be clicked to continue!")

    def keep_cart_tab_open(self) -> None:
        key = "cart_tab"
        self.log(key, "moving pointer to keep it open...")
        ActionChains(self.browser).move_to_element(self.find_element(key)).perform()
        self.log(key, "pointer moved.")

    def set_cart_tab_qnt(self, qnt: int) -> None:
        key = "cart_qnt_input"
        element = self.find_element(key)
        self.log(key, f"setting qnt: {qnt} by replacing the value...")
        ActionChains(self.browser).double_click(element).send_keys(str(qnt)).perform()
        self.log(key, "qnt set.")

    def press_search_postalcode(self) -> None:
        for _ in range(4):
            if self.try_press("postcode_search_button"):
                return
            sleep(0.5)
        raise Exception("expected to be clicked to continue!")

    def set_postal_code(self, postalcode: str) -> None:
        key = "postcode_input"
        element = self.find_element(key)
        self.log(key, f"setting postalcode: {postalcode}...")
        element.clear()
        element.send_keys(postalcode)
        self.log(key, "postalcode set.")

    def collect_delivery_prices(self) -> List[Decimal]:
        key = "shipping_price_labels"
        labels = self.find_elements(key)
        self.log(key, f"got shipping prices: {[la.text for la in labels]}.")
        return [utils.convert_BR_money_to_decimal(la.text) for la in labels]

    # endregion CART_TAB

    def wait_loading_overlay_to_close(self) -> None:
        key = "price_label"
        self.log(key, "waiting to close...")
        for _ in range(20):
            if self.try_press(key):
                self.log(key, "closed.")
                return
            sleep(0.5)
        raise Exception("expected to be clicked to continue!")

    def process(self) -> None:
        data: Dict[int, List[Decimal]] = dict()
        self.browser.maximize_window()
        if self.browser.current_url != self.url:
            self.browser.get(self.url)
        else:
            self.browser.refresh()
        WebDriverWait(self.browser, 10).until(EC.url_to_be(self.url))
        if self.is_reject_cookies_tab_open():
            self.press_reject_cookies()
            self.wait_reject_cookies_bar_close()
        for i in range(1, 4 + 1):
            qnt = i * 6
            if i == 1:
                # we skip setting qnt here and go directly to buy one unit
                self.press_buy()
                self.wait_also_bought_tab_open()
                self.press_check_cart()
                self.wait_also_bought_tab_close()
                self.wait_cart_tab_open()
                self.keep_cart_tab_open()
                self.set_postal_code("28990-772")
            self.set_cart_tab_qnt(qnt)
            self.press_search_postalcode()
            self.wait_loading_overlay_to_close()
            self.wait_cart_tab_close()
            self.press_open_cart()
            self.wait_cart_tab_open()
            self.keep_cart_tab_open()
            data[qnt] = self.collect_delivery_prices()
