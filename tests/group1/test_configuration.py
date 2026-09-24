#pages\test_configuration.py
import pytest
from pages.configuration_page import ConfigurationPage
from utils.helpers import export_simple_download
from config.settings import settings
from pathlib import Path



@pytest.mark.sanity
def test_configuration_tabs_visible(login_wims_application):
    config = ConfigurationPage(login_wims_application)

    config.toggle_theme()
    config.toggle_theme()  # toggle back to original
    config.open_configuration_menu()

    assert config.is_active_schema_visible()
    assert config.is_notification_gateway_visible()
    assert config.is_site_properties_visible()
    assert config.is_subscription_details_visible()
    assert config.is_reference_documents_visible()

@pytest.mark.sanity
def test_active_data_schema_update(login_wims_application):
    config = ConfigurationPage(login_wims_application)
    
    config.toggle_theme()
    config.toggle_theme()  # toggle back to original
    config.go_to_active_data_schema()

    config.select_live_schema()
    config.decrease_retention_days(2)
    config.save_configuration()

    config.increase_retention_days(2)
    config.save_configuration()

    config.select_archived_schema()
    config.decrease_retention_days(1)
    config.save_configuration()


# @pytest.mark.sanity
# def test_notification_gateway(login_wims_application):
#     config = ConfigurationPage(login_wims_application)

#     config.go_to_notification_gateway()

#     config.test_sms_gateway()
#     config.test_email_gateway()
#     config.reset_notification_gateway()
#     config.save_configuration()

@pytest.mark.sanity
def test_site_properties_export(login_wims_application):
    config = ConfigurationPage(login_wims_application)

    config.go_to_site_properties()

    # Excel Export
    config.export_button.click()
    export_simple_download(login_wims_application, "Excel")

    excel_files = list(Path(settings.DOWNLOADS_DIR).glob("*.xls*"))
    assert excel_files, "No Excel file downloaded"

    # PDF Export
    config.export_button.click()
    export_simple_download(login_wims_application, "PDF")

    pdf_files = list(Path(settings.DOWNLOADS_DIR).glob("*.pdf"))
    assert pdf_files, "No PDF file downloaded"


@pytest.mark.sanity
def test_site_properties_grid_interactions(login_wims_application):
    """
    Sanity check to verify Site Properties grid supports:
    - Edit action availability
    - Column tooltips
    """
    config = ConfigurationPage(login_wims_application)

    config.go_to_site_properties()

    assert config.is_site_properties_edit_action_available()
    assert config.verify_site_properties_tooltips()


@pytest.mark.sanity
def test_reference_documents(login_wims_application, test_data):
    config = ConfigurationPage(login_wims_application)

    ref_data = test_data["reference_documents"]["sanity"]

    config.go_to_reference_documents()

    config.add_reference_document(
        group_name=ref_data["group_name"],
        title=ref_data["title"],
        description=ref_data["description"],
        link=ref_data["link"]
    )
    assert config.is_reference_document_save_successful()

@pytest.mark.skip(reason="Wayside Data Subscription Details feature is under development and not ready for testing")
def test_wayside_data_subscription(login_wims_application, test_data):
    config = ConfigurationPage(login_wims_application)

    sub_data = test_data["wayside_subscription"]["sanity"]

    config.go_to_subscription_details()

    assert config.add_wayside_subscription(sub_data)


@pytest.mark.skip(reason="Wayside Data Subscription Details feature is under development and not ready for testing")
def test_wayside_subscription_without_description(login_wims_application, test_data):
    config = ConfigurationPage(login_wims_application)

    sub_data = test_data["wayside_subscription"]["sanity"].copy()
    sub_data["description"] = ""   # invalid case

    config.go_to_subscription_details()

    result = config.add_wayside_subscription(sub_data)

    assert result is False




