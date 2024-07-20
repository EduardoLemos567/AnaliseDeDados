from selenium.webdriver.chrome.options import Options as DriveOptions
from selenium.webdriver.chrome.service import Service as DriveService
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


def do():
    chrome_driver_path = "D:\\Program Files\\ChromeDriver\\chromedriver.exe"
    chrome_options = DriveOptions()
    # chrome_options.add_argument("--headless")
    service = DriveService(executable_path=chrome_driver_path)
    print("connection created and opened")
    driver = ChromeDriver(service=service, options=chrome_options)

    try:
        driver.maximize_window()
        driver.get("https://graphtoy.com/")
        sleep(2)
        f1 = driver.find_element(By.CSS_SELECTOR, "input#formula1")
        f1.send_keys("abdefgh")
        sleep(2)
        f2 = driver.find_element(By.CSS_SELECTOR, "input#formula2")
        f2.clear()
        f2.send_keys("abdefgh")
        sleep(2)
        f2 = driver.find_element(By.CSS_SELECTOR, "input#formula2")
        f2.clear()
        f2.send_keys("abdefgh")
        actions = ActionChains(driver)
        actions.send_keys_to_element(f2, "1234").perform()
        sleep(2)
        actions.send_keys_to_element(f2, "98765").perform()
        sleep(2)
        actions.double_click(f2).send_keys_to_element(f2, "zzz98765").perform()
        sleep(2)
        actions.double_click(f2).send_keys("yyy98765").perform()
        sleep(2)
        # e = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/ul/li[3]")
        # actions = ActionChains(driver)
        # actions.scroll_to_element(e).perform()
        input("press enter to finish")

    finally:
        driver.quit()
        print("connection closed and exited")


if __name__ == "__main__":
    do()
