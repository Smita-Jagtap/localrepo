#\tests\conftest.py
import pytest
import logging
import os
import requests
from datetime import datetime
from config.settings import settings
from utils.screenshot_handler import capture_screenshot
from pages.login_page import LoginPage
from config.environment import env
from playwright.sync_api._generated import Page


@pytest.fixture
def load_application(page: Page):
    """
    Provides a LoginPage instance with the login page already loaded.
    This avoids repeating navigation in every test while keeping tests isolated.
    """
    login_page = LoginPage(page)
    login_page.navigate(env.get_base_url())
    return login_page

@pytest.fixture(scope="session", autouse=True)
def check_app_reachable():
    from config.environment import env
    try:
        requests.get(env.get_base_url(), timeout=10, verify=False)
    except Exception:
        pytest.exit(
            "\n Application not reachable. VPN may be disconnected.\n",
            returncode=1
        )

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    os.makedirs(settings.LOGS_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.get_log_file_path()),
            logging.StreamHandler()
        ]
    )

@pytest.fixture(autouse=True)
def init_test_logger(request):
    logger = logging.getLogger(request.node.name)
    logger.info(f"Starting execution of {request.node.name}")
    yield
    logger.info(f"Finished execution of {request.node.name}")

@pytest.fixture(scope="session")
def test_data():
    from utils.data_utils import load_test_data
    return load_test_data()

@pytest.fixture(scope="session")
def login_wims_application(browser, test_data):

    page = browser.new_page(ignore_https_errors=True)
    login_page = LoginPage(page)
    user = test_data["users"]["valid_user"]
    login_page.navigate(env.get_base_url())
    login_page.login(user["username"], user["password"])
    yield page
    page.close()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": None, #default browser size
        "ignore_https_errors": True,
    }



# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     if report.when == "call" and report.failed:
#         page = item.funcargs.get("page", None)
#         if page:
#             screenshot_path = capture_screenshot(page, item.name)
#             logging.getLogger(item.name).error(f"Test failed. Screenshot saved to {screenshot_path}")
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("login_wims_application")
        if page:
            screenshot_path = capture_screenshot(page, item.name)
            logging.getLogger(item.name).error(f"Test failed. Screenshot saved to {screenshot_path}")