# tests/group1/test_user_management.py

import pytest
from pages.user_management_page import UserManagementPage
from utils.download_utils import export_excel


# ==================================================
# GROUPS — SANITY SAFE
# ==================================================

@pytest.mark.sanity
def test_groups_page_visible(login_wims_application):
    """
    Tests if the groups page is visible after logging in.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_groups()
    assert um.grid.is_visible()


@pytest.mark.sanity
def test_add_group(login_wims_application):
    """
    Tests the functionality of adding a new group.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_groups()
    um.add_group("group_sanity", "sanity test group")
    assert um.page.get_by_text("group_sanity").is_visible()


@pytest.mark.regression
def test_edit_group(login_wims_application):
    """
    Tests the functionality of editing an existing group.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_groups()
    um.edit_first_group()
    assert um.page.get_by_text("is updated").is_visible()


@pytest.mark.regression
def test_delete_group(login_wims_application):
    """
    Tests the functionality of deleting a group.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_groups()
    um.delete_first_group()
    assert um.page.get_by_text("is deleted").is_visible()


@pytest.mark.sanity
def test_export_groups_excel(login_wims_application):
    """
    Tests the functionality of exporting groups to an Excel file.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_groups()
    file = um.export_excel()
    assert file.exists()
    assert file.stat().st_size > 0


# ==================================================
# USERS — SANITY SAFE
# ==================================================

@pytest.mark.sanity
def test_users_page_visible(login_wims_application):
    """
    Tests if the users page is visible after logging in.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_users()
    assert um.grid.is_visible()


@pytest.mark.sanity
def test_add_user(login_wims_application):
    """
    Tests the functionality of adding a new user.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_users()
    um.add_user({
        "login_id": "user_sanity",
        "first_name": "Sanity",
        "last_name": "User",
        "company": "Test",
        "title": "Engineer",
        "email": "user@test.com",
        "mobile": "9999999999",
        "work_phone": "8888888888"
    })
    assert um.page.get_by_text("user_sanity").is_visible()


@pytest.mark.regression
def test_edit_user(login_wims_application):
    """
    Tests the functionality of editing an existing user.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_users()
    um.edit_first_user()
    assert um.page.get_by_text("is updated").is_visible()


@pytest.mark.regression
def test_delete_user(login_wims_application):
    """
    Tests the functionality of deleting a user.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_users()
    um.delete_first_user()
    assert um.page.get_by_text("is deleted").is_visible()


@pytest.mark.sanity
def test_export_users_excel(login_wims_application):
    """
    Tests the functionality of exporting users to an Excel file.
    """
    um = UserManagementPage(login_wims_application)
    um.go_to_users()
    file = um.export_excel()
    assert file.exists()
    assert file.stat().st_size > 0
