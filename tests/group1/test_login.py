# tests/group1/test_login.py

from typing import Any
import pytest
from pages.base_page import BasePage
from utils.helpers import assert_login_failed

# ==============================================================================
# Sanity tests
# ==============================================================================

@pytest.mark.sanity
def test_invalid_login(load_application, test_data: Any):
    """Verify login fails for an invalid user."""
    user = test_data["users"]["invalid_user"]

    load_application.login(user["username"], user["password"])
    assert_login_failed(load_application.page, load_application)


@pytest.mark.sanity
def test_valid_login(load_application, test_data: Any):
    """Basic sanity check for a valid logged-in session."""
    user = test_data["users"]["valid_user"]

    load_application.login(user["username"], user["password"])

    load_application.assert_url_contains("home")


@pytest.mark.sanity
def test_logout_ends_user_session(load_application, test_data: Any):
    """Verify that user can log out and session is terminated."""
    user = test_data["users"]["valid_user"]

    load_application.login(user["username"], user["password"], user_type="external")

    load_application.assert_url_contains("home")

    # Logout via Page Object
    load_application.logout_user()
    load_application.assert_url_contains("user-logout")

