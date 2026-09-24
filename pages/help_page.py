from playwright.sync_api import Page, expect
import os


class HelpMenuPage:
    def __init__(self, page: Page):
        self.page = page

    # ========= LOCATORS =========
        self.help_menu = page.get_by_text("Help", exact=True)
        self.help_guide = page.get_by_text("Help Guide")
        self.abbreviations = page.get_by_text("Abbreviations, Terms, Definitions and Legends")
        self.user_manual = page.get_by_text("User Manual")
        self.reference_docs = page.get_by_text("Reference Documents and Web Pages")
        self.disclaimer = page.get_by_text("Disclaimer")
        self.about_wims = page.get_by_text("About WIMS")

        # ========== DISCLAIMER POPUP ==========
        self.disclaimer_title = page.get_by_role("heading", name="WIMS Disclaimer - Annual User Agreement")
        self.close_button = page.locator("button.disclaimer-btn-close")

        # ========== PROFILE / LOGOUT ==========
        self.profile_icon = page.get_by_role("img")
        self.logout_option = page.get_by_role("menuitem", name="Log Out")

    # ========= Actions =========

    def hover_on_help_menu(self):
        # Hover over Help menu and display
        self.help_menu.hover()

    def verify_help_menu_visible(self):
        # Hover over Help menu to display all options
            expect(self.help_menu).to_be_visible()
            expect(self.help_menu).to_be_enabled()

    def verify_all_help_options_visible(self):
        # Verifies that all 6 help options are visible after hover
        self.hover_on_help_menu()
        expect(self.help_guide).to_be_visible()
        expect(self.abbreviations).to_be_visible()
        expect(self.user_manual).to_be_visible()
        expect(self.reference_docs).to_be_visible()
        expect(self.disclaimer).to_be_visible()
        expect(self.about_wims).to_be_visible()

    def open_help_guide(self):
        self.hover_on_help_menu()
        with self.page.context.expect_page() as new_page:
            self.help_guide.click()
        return new_page.value

    def open_abbreviations(self):
        self.hover_on_help_menu()
        with self.page.context.expect_page() as new_page:
            self.abbreviations.click()
        return new_page.value

    def download_user_manual(self,download_dir: str)->str:
        self.hover_on_help_menu()

        with self.page.expect_download(timeout=50000) as download_info:
            self.user_manual.click()

        download = download_info.value
        file_path = os.path.join(download_dir, download.suggested_filename)
        download.save_as(file_path)

        return file_path

    def open_reference_documents(self):
        self.hover_on_help_menu()
        self.reference_docs.click()

    def open_disclaimer(self):
        self.hover_on_help_menu()
        self.disclaimer.click()

    def close_disclaimer(self):
        self.close_button.click()

    def open_about_wims(self):
        self.hover_on_help_menu()
        with self.page.context.expect_page() as new_page:
            self.about_wims.click()
        return new_page.value





