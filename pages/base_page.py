import re
from playwright.sync_api import Page, expect

class BasePage:
    """Base Page class holding common utilities for all pages."""
    
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigates to the specified URL."""
        self.page.goto(url)

    def wait_for_load_state(self, state="networkidle"):
        """Waits for the specified load state."""
        self.page.wait_for_load_state(state)

    def get_title(self) -> str:
        """Returns the current page title."""
        return self.page.title()

    def assert_url_contains(self, text: str):
        """Asserts that the current URL contains the given text."""
        expect(self.page).to_have_url(re.compile(f".*{text}.*"))
