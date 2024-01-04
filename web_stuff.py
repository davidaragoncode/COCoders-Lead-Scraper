from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def has_careers_page(url)->bool:
    try:
        # Create a new instance of the Firefox webdriver
        driver = webdriver.Firefox()

        # Open the provided URL
        driver.get(url)

        # Check if the "Careers" keyword is present in the page source
        careers_found = "careers" in driver.page_source.lower()

        return careers_found

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser window
        driver.quit()

# Example usage
# url_to_check = "https://ssreng.com/"
# result = has_careers_page(url_to_check)
#
# if result:
#     print(f"The website {url_to_check} has a 'Careers' page.")
#
# else:
#     print(f"The website {url_to_check} does not have a 'Careers' page.")