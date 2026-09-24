import pytest
from playwright.sync_api import sync_playwright, expect
import os
from pages.help_page import HelpMenuPage
from pages.login_page import LoginPage
from config.environment import env
from utils.data_utils import load_test_data


@pytest.mark.sanity
def test_help(login_wims_application):
    # Verify Help menu and all help options are visible
    help_page = HelpMenuPage(login_wims_application)
    help_page.verify_help_menu_visible()
    help_page.verify_all_help_options_visible()


@pytest.mark.sanity
def test_helpguide(login_wims_application):
    help_page = HelpMenuPage(login_wims_application)
    help_guide_page = help_page.open_help_guide()
    help_guide_page.wait_for_load_state("domcontentloaded")  #added

    #  assertion->verify title
    expect(help_guide_page).to_have_title("WIMS")
    help_guide_page.close()


@pytest.mark.sanity
def test_abbreviations(login_wims_application):
    # Verify Abbreviations page opens in new tab with correct title
    help_page = HelpMenuPage(login_wims_application)
    abbreviations_page = help_page.open_abbreviations()
    abbreviations_page.wait_for_load_state("domcontentloaded")

    # verifying visible text
    expect(abbreviations_page.locator("div.title-area span.title")).to_have_text(
        "Abbreviations, Terms, Definitions and Legends")
    abbreviations_page.close()


@pytest.mark.sanity
def test_user_manual_download(login_wims_application):
    # Verify User Manual is downloaded successfully"

    page = login_wims_application
    help_page = HelpMenuPage(page)

    # Save downloads in the same test folder
    test_dir = os.path.dirname(__file__)
    downloaded_file = help_page.download_user_manual(test_dir)

    # Assertions
    assert os.path.exists(downloaded_file), "User Manual was not downloaded"
    print(f"User Manual downloaded successfully to: {downloaded_file}")


@pytest.mark.sanity
def test_reference_documents(login_wims_application):
    # Verify Reference Documents opens in new tab and title is correct
    help_page = HelpMenuPage(login_wims_application)
    help_page.open_reference_documents()
    login_wims_application.wait_for_load_state("domcontentloaded")
    # Assertion
    expect(
        login_wims_application.locator(
            "div.container-fluid.reference-documents span.title")
    ).to_have_text("Reference Documents and Web Pages")


@pytest.mark.sanity
def test_disclaimer(login_wims_application):
    # Verify Disclaimer modal opens and closes
    help_page = HelpMenuPage(login_wims_application)

    # Open Disclaimer modal
    help_page.open_disclaimer()
    expect(help_page.disclaimer_title).to_be_visible(timeout=5000)

    # Verify close button
    expect(help_page.close_button).to_be_visible()
    expect(help_page.close_button).to_be_enabled()

    # Close modal
    help_page.close_disclaimer()

@pytest.mark.sanity
def test_about_wims(login_wims_application):
    # Verify About WIMS opens in new tab and title is correct
    help_page = HelpMenuPage(login_wims_application)
    about_wims_page = help_page.open_about_wims()
    about_wims_page.wait_for_load_state("domcontentloaded")

    # Assert visible content, not title
    expect(
        about_wims_page.locator("//div[contains(@class,'about-wims-title')]//span[text()='About WIMS']")
    ).to_be_visible()

    about_wims_page.close()


# logout
@pytest.mark.sanity
def test_logout(login_wims_application):
    page = login_wims_application
    login_page = LoginPage(page)
    login_page.account_icon = login_page.account_icon.first
    login_page.logout_user()


