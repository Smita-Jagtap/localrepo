from pages.base_page import BasePage
from playwright.sync_api import expect

class UserProfilePage(BasePage):
    """Page Object for the User Profile Page."""
    
    def __init__(self, page):
        super().__init__(page)
        # Locators
        self.profile_header = page.locator("h2.profile-header")
        self.first_name_input = page.locator("input[name='firstName']")
        self.last_name_input = page.locator("input[name='lastName']")
        self.save_button = page.locator("button#save-profile")
        self.success_toast = page.locator(".toast-success")

    def verify_on_profile_page(self):
        expect(self.profile_header).to_be_visible()

    def update_name(self, first_name, last_name):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.save_button.click()

    def verify_update_success(self):
        expect(self.success_toast).to_be_visible()
