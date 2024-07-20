from logging import Logger
from selenium.webdriver.chrome.options import Options as DriveOptions
from selenium.webdriver.chrome.service import Service as DriveService
from selenium.webdriver import Chrome as ChromeDriver

logger: Logger | None = None


def setup_driver() -> ChromeDriver:
    chrome_driver_path = "D:\\Program Files\\ChromeDriver\\chromedriver.exe"
    chrome_options = DriveOptions()
    # chrome_options.add_argument("--headless")
    service = DriveService(executable_path=chrome_driver_path)
    if logger:
        logger.info("connection created and opened")
    driver = ChromeDriver(service=service, options=chrome_options)
    return driver


def close_driver(driver: ChromeDriver | None) -> None:
    if not isinstance(driver, ChromeDriver):
        return
    driver.quit()
    del driver
    if logger:
        logger.info("connection closed")
