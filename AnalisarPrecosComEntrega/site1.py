from logging import Logger
from time import sleep
from typing import List
from decimal import Decimal
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
)
import utils

logger: Logger | None = None


class Site1:
    _url = "https://www.lojarelvaverde.com.br/bebida-de-castanha-de-caju-sabor-leite-sem-leite-possible-1l-p3123"

    _selectors = {
        "price_label": "#product-details > b > div > div.procuct-detail > div.product-values > div > div.price > b",
        "buy_button": "#product-details > b > div > div.procuct-detail > b > div.botao_comprar > div > a > button",
        "front_qnt_input": "#quantity",
        "cart_qnt_input": "#cart-items > #item-3123 * input",
        "check_cart_button": ".fancybox-content > .popup-product-added * div.actions.flex > button.w-100.btn-primary.btn.cart",
        "open_cart_button": ".sidecart-button",
        "postcode_input": "#cep",
        "postcode_search_button": "#btn-calc-frete > i > svg > path",
        "shipping_price_labels": "#side-cart > div.cart-total.flex > div.shopping-cart-shipping.flex.w-100 > dl > dl.shipping-options > .option > * > .price",
        "reject_cookie_button": "#adopt-reject-all-button",
    }

    def __init__(self, driver: ChromeDriver) -> None:
        self._driver = driver
        self._actions = ActionChains(driver)
        self._waiter = WebDriverWait(driver, 40, 0.2)
        self._elements = dict.fromkeys(self._selectors.keys())

    def _load_url(self) -> None:
        self._driver.get(self._url)
        if logger:
            logger.debug(
                f"site loaded {utils.get_domain_from_url(self._driver.current_url)}"
            )

    def _get_element(self, key: str) -> WebElement:
        if key in self._elements:
            element = self._elements[key]
        if not isinstance(element, WebElement):
            self._elements[key] = element = self._waiter.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self._selectors[key]))
            )
        return element

    def _get_elements(self, key: str) -> List[WebElement]:
        if key in self._elements:
            elements: List[WebElement] | None = self._elements[key]
        if not isinstance(elements, list):
            self._elements[key] = elements = self._waiter.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, self._selectors[key])
                )
            )
        return elements

    def _scroll_until_visible(self, key: str) -> None:
        element: WebElement = self._get_element(key)
        self._actions.scroll_to_element(element).perform()
        self._waiter.until(EC.visibility_of(element))

    def _click_scrolled_element(self, key: str) -> None:
        self._scroll_until_visible(key)
        element: WebElement = self._get_element(key)
        self._waiter.until(EC.element_to_be_clickable(element))
        element.click()

    def _click_button(self, key: str) -> None:
        self._click_scrolled_element(key)

    def _set_input(self, key: str, value: str) -> None:
        input = self._get_element(key)
        input.clear()
        input.send_keys(value)

    def _set_input_replace(self, key: str, value: str) -> None:
        input = self._get_element(key)
        self._actions.double_click(input).send_keys(value).perform()
        if logger:
            logger.debug("input_safer done")

    def _read_element(self, key: str) -> str:
        return self._get_element(key).text

    def _get_price(self) -> Decimal:
        return utils.convert_money_to_decimal(self._read_element("price_label"))

    def _set_qnt(self, qnt: int) -> None:
        self._set_input("front_qnt_input", str(qnt))

    def _press_buy(self) -> None:
        self._click_button("buy_button")

    def _is_shipping_tab_open(self) -> bool:
        input = self._get_element("postcode_input")
        return input.is_displayed()

    def _open_shipping_tab(self) -> None:
        # is open ? finish early
        if self._is_shipping_tab_open():
            return
        # open it
        self._click_button("open_cart_button")
        # wait until opened
        self._waiter.until(
            EC.element_to_be_clickable(self._get_element("postcode_input"))
        )
        # ensure it does not close by setting the mouse at it
        self._actions.move_to_element(self._get_element("postcode_input"))
        assert self._is_shipping_tab_open(), "shipping tab was not opened"

    def _press_check_cart(self) -> None:
        self._click_button("check_cart_button")

    def _collect_shipping_costs(self) -> List[Decimal]:
        labels = self._get_elements("shipping_price_labels")
        return [utils.convert_money_to_decimal(l.text) for l in labels]

    def _calculate_shipping_first(self, postcode: str) -> List[Decimal]:
        self._open_shipping_tab()
        if self._read_element("postcode_input") != postcode:
            self._set_input("postcode_input", postcode)
        self._click_button("postcode_search_button")
        self._waiter.until(
            EC.element_to_be_clickable(self._get_element("open_cart_button"))
        )
        self._open_shipping_tab()
        return self._collect_shipping_costs()

    def _calculate_shipping(self, qnt: int) -> List[Decimal]:
        self._open_shipping_tab()
        qnt_text = self._read_element("cart_qnt_input")
        if (int(qnt_text) if qnt_text else 0) != qnt:
            self._set_input_replace("cart_qnt_input", str(qnt))
        sleep(1)
        assert self._get_element(
            "cart_qnt_input"
        ).is_displayed(), "cart item is missing"
        self._click_button("postcode_search_button")
        self._waiter.until(
            EC.element_to_be_clickable(self._get_element("open_cart_button"))
        )
        self._open_shipping_tab()
        return self._collect_shipping_costs()

    def process(self) -> dict:
        self._driver.maximize_window()
        if self._driver.current_url != self._url:
            self._load_url()
        self._waiter.until(EC.url_to_be(self._url))
        sleep(1)
        # @TODO: bug, values are typed too fast and wrong, maybe not erased ?
        try:
            self._click_button("reject_cookie_button")
        except NoSuchElementException:
            pass
        data = {}
        shipping_costs = {}
        data["unit_price"] = self._get_price()
        for i in range(1, 4 + 1):
            qnt = 6 * i
            if i == 1:
                self._set_qnt(qnt)
                self._press_buy()
                self._waiter.until(
                    EC.element_to_be_clickable(self._get_element("check_cart_button"))
                )
                self._press_check_cart()
                costs = self._calculate_shipping_first("28990-772")
            else:
                costs = self._calculate_shipping(qnt)
            shipping_costs[qnt] = costs
        data["shipping_costs"] = shipping_costs
        return data
