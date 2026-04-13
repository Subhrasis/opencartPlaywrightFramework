from playwright.sync_api import Page
from pages.logout_page import LogoutPage

class HomePage:
    def __init__(self, page:Page):
        """
        Constructor to initialize the Playwright page object
        and define all necessary locators.
        """
        self.page = page

        # ===== Locators =====
        # Using Playwright's 'locator' method to identify UI elements
        self.lnk_my_account = self.page.locator("span.d-none:has-text('My Account')")
        self.lnk_register = self.page.locator("a.dropdown-item:has-text('Register')")
        self.lnk_login = self.page.locator("a.dropdown-item:has-text('Login')")
        self.txt_search_box = self.page.locator("input[placeholder='Search']")
        self.btn_search = self.page.locator("button[class='btn btn-light btn-lg'][type='submit']")
        self.lnk_logout = self.page.locator('a:has-text("Logout")')

        # ===== Action Methods =====
        # Each method represents a user interaction on the page

    def get_homepage_title(self):
        """Return the title of the Home Page."""
        title = self.page.title()
        return title

    def click_my_account(self):
        try:
            self.lnk_my_account.click()
        except Exception as e:
            print(f" Exception while clicking 'My Account' : {e}")
            raise

    def click_register(self):
        """Click on the 'Register' link under My Account."""
        try:
            self.lnk_register.click()
        except Exception as e:
            print(f" Exception while clicking 'Register': {e}")
            raise

    def click_login(self):
        """Click on the 'Login' link under My Account."""
        try:
            self.lnk_login.click()
        except Exception as e:
            print(f" Exception while clicking 'Login': {e}")
            raise

    def enter_product_name(self, product_name: str):
        """Enter the product name into the search input box."""
        try:
            self.txt_search_box.fill(product_name)
        except Exception as e:
            print(f" Exception while entering product name '{product_name}': {e}")
            raise

    def click_search(self):
        """Click on the search button to initiate the product search."""
        try:
            self.btn_search.click()
        except Exception as e:
            print(f" Exception while clicking 'Search' button: {e}")
            raise

    def click_logout(self):
        """Click on the 'Logout' link under My Account."""
        try:
            self.lnk_logout.click()
            return LogoutPage(self.page)
        except Exception as e:
            print(f" Exception while clicking 'Logout': {e}")
            raise
