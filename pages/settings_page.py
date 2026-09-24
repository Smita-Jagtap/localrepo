from pages.base_page import BasePage
from playwright.sync_api import expect

class SettingsPage(BasePage):
    """Page Object for the Settings Page."""
    
    def __init__(self, page):
        super().__init__(page)
        # Locators
        self.settings_header = page.locator("h2.settings-header")
        self.theme_dropdown = page.locator("select[name='theme']")
        self.notifications_toggle = page.locator("input[name='notifications']")
        self.save_button = page.locator("button#save-settings")

    def verify_on_settings_page(self):
        expect(self.settings_header).to_be_visible()

    def update_settings(self, theme="dark", enable_notifications=True):
        self.theme_dropdown.select_option(theme)
        if enable_notifications:
            self.notifications_toggle.check()
        else:
            self.notifications_toggle.uncheck()
        self.save_button.click()
