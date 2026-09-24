from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Page Object for the Login Page."""
    
    def __init__(self, page):
        super().__init__(page)
        self.external_user_checkbox = page.locator("#externalUser")
        self.internal_user_checkbox = page.locator("#internalUser")
        self.username_input = page.locator('input[name="loginId"]')
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.get_by_role("heading", name="Error")
        self.account_icon=page.locator("img[src*='account_circle']")
        self.logout_option= page.locator("text=Log Out")
    
    def select_external_user(self):
        """
        Select the External user option if it is not already selected.
        Works for radio buttons as well as checkboxes.
        """

        # Wait until the external user input exists and is visible
        # self.external_user_checkbox.wait_for(state="visible", timeout=10000)

        # Select only if not already selected
        if not self.external_user_checkbox.is_checked():
            self.external_user_checkbox.click()

    def login(self, username, password, user_type="external"):
        """Perform login using the standard External User flow."""

        logger.info("Starting login flow")

        # self.page.wait_for_load_state("domcontentloaded", timeout=15000)
        logger.info("Login page loaded")

        self.select_external_user()
        logger.info("External user selected")

        # self.username_input.first.wait_for(state="visible", timeout=10000)
        self.username_input.first.fill(username)
        logger.info("Username entered")

        self.password_input.first.fill(password)
        logger.info("Password entered")

        self.login_button.click()
        logger.info("Login form submitted")

    def get_error_message(self)-> str:
        """Return error message text if present, else empty string."""
        error_heading = self.page.get_by_role("heading", name="Error")
        if error_heading.is_visible():
            return error_heading.text_content().strip()
        return ""
    
    def logout_user(self):
        """Log out the current user via profile dropdown."""
        self.account_icon.click()
        self.logout_option.click()


