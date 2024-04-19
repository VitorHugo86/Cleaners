import time
import os
import logging
from pychrome import Chrome
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class PythonCleaner:
    def __init__(self, target_directories, temporary_extensions):
        self.target_directories = target_directories
        self.temporary_extensions = temporary_extensions
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def welcome(self) -> None:
        print('******************************************************************')
        print('****************      PYTHON_CLEANER   ****************************')
        print('*******************************************************************')
        print('----------------        WELCOME        ----------------------------')
        time.sleep(3)
        print('\nCleaning .................')

    def clean_temporary_files(self):
        """
        Cleans temporary files from the target directories.
        """
        for target_directory in self.target_directories:
            try:
                with os.scandir(target_directory) as it:
                    for entry in it:
                        if entry.is_file() and entry.name.endswith(tuple(self.temporary_extensions)):
                            file_path = os.path.join(target_directory, entry.name)
                            try:
                                os.remove(file_path)
                                print(f"File removed: {file_path}")
                                self.logger.info(f"File removed: {file_path}")
                            except Exception as e:
                                print(f"Failed to remove file {file_path}: {e}")
                                self.logger.error(f"Failed to remove file {file_path}: {e}")
            except Exception as e:
                print(f"Error cleaning directory {target_directory}: {e}")
                self.logger.error(f"Error cleaning directory {target_directory}: {e}")

    def clean_chrome_cache(self):
        try:
            chrome = Chrome()
            chrome.clear_cache()
            chrome.close()
            print("Google Chrome cache cleared.")
        except Exception as e:
            print(f"Error clearing Google Chrome cache: {e}")

    def clean_firefox_cookies(self):
        try:
            options = FirefoxOptions()
            options.headless = True  # Run the browser in headless mode (no GUI)
            driver = webdriver.Firefox(options=options)
            driver.get('about:preferences#privacy')  # Open Firefox privacy settings
            driver.find_element_by_id('clearOnClose-checkbox').click()  # Check the option to clear cookies on close
            driver.find_element_by_id('clearOnClose-checkbox').click()  # Uncheck the option to ensure it's unchecked
            driver.find_element_by_id('cookieExceptions').click()  # Open cookie exceptions
            driver.find_element_by_id('clearButton').click()  # Click the button to clear all cookies
            driver.close()
            print("Mozilla Firefox cookies cleared.")
        except Exception as e:
            print(f"Error clearing Mozilla Firefox cookies: {e}")

def main():
    target_directories = [
        "C:\\Windows\\Temp",  # Windows temporary directory
        os.path.join(os.getenv('APPDATA'), 'Local', 'Temp')  # User's local temporary directory
    ]
    temporary_extensions = ['.tmp', '.temp', '.bak', '.log', '.json', '.gz', '.LOG', '.txt', '.MTX', '.Mtx']  # Add other extensions as needed

    cleaner = PythonCleaner(target_directories, temporary_extensions)
    cleaner.welcome()
    cleaner.clean_temporary_files()
    cleaner.clean_chrome_cache()
    cleaner.clean_firefox_cookies()

if __name__ == "__main__":
    main()
