import re
import pytest
from playwright.sync_api import expect
from pages.analysis_page import AnalysisPage

@pytest.mark.sanity
def test_analysis_navigation(login_wims_application):
    """Test whether heading is visible in Analysis page."""
    analysis_page = AnalysisPage(login_wims_application)
    analysis_page.navigate_to_step_change_vehicles()
    analysis_page.verify_step_change_vehicles()


@pytest.mark.sanity
def test_step_change_table(login_wims_application):
    """Test whether data is present in Step Change Details table."""
    analysis_page = AnalysisPage(login_wims_application)
    # To navigate to analysis - Step Change Vehicles page
    analysis_page.navigate_to_step_change_vehicles()
    #To verify whether data is present in step change vehicles table
    analysis_page.verify_step_change_table()


@pytest.mark.sanity
def test_history_button(login_wims_application):
    """Test the History button in the Step Change Details table."""
    analysis_page = AnalysisPage(login_wims_application)
    analysis_page.navigate_to_step_change_vehicles()

    history_page = analysis_page.click_history_button()

    # Correct validation
    expect(history_page).to_have_url(  # expect confirms history page opened correctly
        re.compile("vehicle-pass-history-tabular")  # Uses regex because URL contains dynamic values
    )
    history_page.wait_for_timeout(5000)

    history_page.close()


@pytest.mark.sanity
def test_vphg_button(login_wims_application):
    """Test the VPHG button in the Step Change Details table."""
    analysis_page = AnalysisPage(login_wims_application)
    analysis_page.navigate_to_step_change_vehicles()

    # Click VPHG button
    vphg_page = analysis_page.click_vphg_button()

    # Validate popup opened

    expect(vphg_page).to_have_url(  # Verifies that the popup page opened successfully.
        re.compile("pop-up")  # Uses regex because the URL contains dynamic values.
    )
    vphg_page.close()

@pytest.mark.sanity
def test_site_properties_export(login_wims_application):
    analysis_page = AnalysisPage(login_wims_application)
    analysis_page.navigate_to_step_change_vehicles()

    excel_download = analysis_page.export_site_properties_excel()
    assert excel_download is not None
    assert excel_download.suggested_filename.lower().endswith((".xls", ".xlsx"))

    pdf_download = analysis_page.export_site_properties_pdf()
    assert pdf_download is not None
    assert pdf_download.suggested_filename.lower().endswith(".pdf")

@pytest.mark.sanity
def test_speed_distribution_graph(login_wims_application):
    """Test Speed Distribution Graph Page."""
    analysis_page = AnalysisPage(login_wims_application)

    # To navigate to Analysis-Speed Distribution Graph page
    analysis_page.navigate_to_speed_distribution_graph()

    #To verify heading of the opened page
    analysis_page.verify_speed_distribution_graph()

    #To verify filters of the speed distribution graph
    analysis_page.verify_speed_distribution_graph_filters()
