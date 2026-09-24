# utils/helpers.py

from cProfile import label
import logging
from datetime import datetime
import re
from pages.login_page import LoginPage
from config.environment import env
from playwright.sync_api import Locator, Page, expect
from config.settings import settings
from utils.screenshot_handler import capture_screenshot

logger = logging.getLogger(__name__)


def login_user(page, username, password, navigate=True):
    
    logger.info(f"Logging in user '{username}' ")
    login_page = LoginPage(page)

    if navigate:
        login_page.navigate(env.get_base_url())

    login_page.login(username, password)

    # HARD STOP: wait until Train Pass View page
    page.wait_for_url("**/home/views/train-pass-view", timeout=50000)
    expect(page).to_have_url(re.compile(r"home/views/train-pass-view"))

    logger.info(f"Login successful. Landed on: {page.url}")
    return page


# ----------------------------------------------------------------------
# Authentication-related assertion helpers
# ----------------------------------------------------------------------

def assert_login_failed(page, login_page, expected_text=None):
    """Assert that login attempt failed."""

    page.wait_for_timeout(500)  # Allow SPA routing to settle
    url = page.url.lower()

    # User must not be logged in
    assert "dashboard" not in url
    assert "home/views" not in url

    # Failure is confirmed by error state (URL or UI)
    assert (
        "/error" in url
        or login_page.is_login_error_visible()
    ), f"Expected login failure, got page URL {page.url}"

    if expected_text:
        assert expected_text.lower() in login_page.get_error_message().lower()

#----------------------------------------------------------------------
# UI interaction helpers- Tooltip verification
#----------------------------------------------------------------------
def verify_tooltip(page: Page,page_tooltip_set):
   
    for header_text, tooltip_text in page_tooltip_set:
            header = page.locator(
                f"//span[normalize-space()='{header_text}']"
            )
            logger.info(f"Verifying tooltip: {tooltip_text}")

            expect(header).to_be_visible(timeout=5000)

            header.hover()

            tooltip = page.locator(
            f"//span[normalize-space()='{tooltip_text}']"
            )

            expect(tooltip).to_be_visible(timeout=5000)

#-------------------------------------------------------------------
# Export flow helper - date range selection and export trigger
#-------------------------------------------------------------------

def format_date(d):
    return f"{d.strftime('%B')} {d.day}, {d.strftime('%Y')}"

def export_with_date_range(page: Page, start_date,end_date, export_format):
    """
    Generic export helper WITH date range.

    Args:
        page (Page)
        "start_date": "May 1, 2025",
        "end_date": "May 10, 2025",
        "format": "Excel/PDF"

    Returns:
        list: downloaded file paths
    """

    downloaded_files = []
    # Select Start Date
    page.get_by_role("button", name="Select").first.click()
    start_cell = page.locator(".dx-calendar").last.get_by_label(start_date)
    expect(start_cell).to_be_visible()
    start_cell.click()

    # Select End Date
    page.get_by_role("button", name="Select").nth(1).click()
    end_cell = page.locator(".dx-calendar").last.get_by_label(end_date)
    expect(end_cell).to_be_visible()
    end_cell.click()

    # Select format
    format_option = page.get_by_text(export_format, exact=True)
    expect(format_option).to_be_visible()
    format_option.click()

    # Final export button
    export_final = page.locator(
            "//div[contains(@class,'dx-overlay-content')]//dx-button"
        ).filter(has_text="Export").first

    expect(export_final).to_be_visible()

    # Download file
    with page.expect_download() as download_info:
            export_final.click()

    download = download_info.value
    file_path = settings.DOWNLOADS_DIR / download.suggested_filename
    download.save_as(file_path)
    logger.info(f"File downloaded: {file_path}")
    downloaded_files.append(file_path)


#-------------------------------------------------------------------
# Export flow helper - without date range selection
#------------------------------------------------------------------- 

def export_simple_download(page: Page, format_name):
    """
    Handles export AFTER export dialog is already opened.

    Args:
        page (Page)
        format_name (str): "Excel" or "PDF"

    Returns:
        list: downloaded file paths
    """

    downloaded_files = []

    # Select format
    format_radio = page.get_by_role("radio", name=format_name)
    expect(format_radio).to_be_visible()
    format_radio.click()

    # Click Download
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Download").click()

    download = download_info.value
    file_path = settings.DOWNLOADS_DIR / download.suggested_filename
    download.save_as(file_path)

    logger.info(f"File downloaded: {file_path}")
    downloaded_files.append(file_path)


def screenshot_capture(page: Page, condition, test_name: str):
    """
    Universal assertion helper that captures screenshot on both PASS and FAIL.
    Usage:
        screenshot_capture(page, title == "Home", "verify_home_page")
    """
    try:
        assert condition, f"Assertion failed for condition: {condition}"
        screenshot_path= capture_screenshot(page, f"{test_name}_PASS")
        logger.info(f"[PASS] {test_name} | Screenshot: {screenshot_path}")

    except AssertionError as e:
        screenshot_path= capture_screenshot(page, f"{test_name}_FAIL")
        logger.error(f"[FAIL] {test_name} | Screenshot: {screenshot_path}")
        raise


def apply_sorting(page: Page):
    """
    Handles sorting AFTER sort dialog is opened.
    Toggles sorting between ascending and descending.
    """
    # ascending 
    ascending = page.get_by_role("button", name="arrowup")
    descending = page.get_by_role("button", name="arrowdown")

    #expect(ascending).to_be_visible()
    #ascending.click()
    #logger.info("Ascending order button clicked")

    #descending
    expect(descending).to_be_visible()
    descending.click()
    logger.info("Descending order button clicked")

    #Click Apply
    apply_button = page.get_by_role("button", name="Apply")
    expect(apply_button).to_be_visible()
    apply_button.click()
    logger.info("Apply button is clicked")

def apply_reset(reset_button):
    """
    Clicks the provided reset button element.
    """
    expect(reset_button).to_be_visible()

    reset_button.click()
    logger.info("Reset button clicked, filters and sorting cleared")


def apply_sort_with_date_range(page, start_date, end_date):

    #START DATE
    page.get_by_role("button", name="Select").first.click()

    start_calendar = page.locator(".dx-calendar").last
    start_calendar.locator(
        f"[aria-label*='{start_date}']:not(.dx-calendar-other-month)"
    ).click()

    page.get_by_role("button", name="Done").first.click()

    #END DATE
    page.get_by_role("button", name="Select").nth(1).click()

    end_calendar = page.locator(".dx-calendar").last
    end_calendar.locator(
        f"[aria-label*='{end_date}']:not(.dx-calendar-other-month)"
    ).click()

    page.get_by_role("button", name="Done").first.click()

def adjust_slider_range(page, from_percent: int, till_percent: int):
    """
    Drag slider handles using actual handle elements.
    """

    # wait for popup
    popup = page.locator(".dx-overlay-content").last
    popup.wait_for()

    # track + handles
    track = popup.locator(".dx-trackbar-wrapper")
    handles = popup.locator(".dx-slider-handle")

    from_handle = handles.nth(0)
    till_handle = handles.nth(1)

    box = track.bounding_box()

    if not box:
        raise Exception("Slider track not found")

    start_x = box["x"]
    y = box["y"] + box["height"] / 2
    width = box["width"]

    # target positions
    from_target = start_x + (width * from_percent / 100)
    till_target = start_x + (width * till_percent / 100)

    # DRAG FROM HANDLE
    from_box = from_handle.bounding_box()
    page.mouse.move(from_box["x"] + 5, from_box["y"] + 5)
    page.mouse.down()
    page.mouse.move(from_target, y)
    page.mouse.up()

    # DRAG TILL HANDLE
    till_box = till_handle.bounding_box()
    page.mouse.move(till_box["x"] + 5, till_box["y"] + 5)
    page.mouse.down()
    page.mouse.move(till_target, y)
    page.mouse.up()

    logger.info(f"Slider set → From {from_percent}% | Till {till_percent}%")
