import pytest
from pages.dashboard_page import DashboardPage
import logging
from utils.helpers import export_with_date_range

logger = logging.getLogger(__name__)


################## Management Overview Page Start #######################

@pytest.mark.sanity
def test_alarms_and_responses_times_table(login_wims_application):
    """Test whether data is present in Overview of Alarms and Responses Times (Today) table."""
    dashboard_page = DashboardPage(login_wims_application)
    # To navigate to  DashboardPage - Management-overview subpage
    dashboard_page.navigate_to_management_overview()
    # To verify whether data is present in Overview of Alarms and Responses Times (Today) table
    dashboard_page.verify_alarms_and_responses_times_table()

@pytest.mark.sanity
def test_alarms_and_responses_times_export(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_management_overview()

    #  Excel Export
    dashboard_page.open_alarms_and_responses_times_table_export_popup()

    #  CRITICAL FIX
    dashboard_page.prepare_calendar_for_helper()

    export_with_date_range(
    page=dashboard_page.page,
    start_date="May 24, 2024",
    end_date="May 18, 2026",
    export_format="Excel"
    )
    dashboard_page.page.keyboard.press("Escape")
    # PDF
    dashboard_page.open_alarms_and_responses_times_table_export_popup()
    dashboard_page.prepare_calendar_for_helper()

    export_with_date_range(
    page=dashboard_page.page,
    start_date="May 24, 2024",
    end_date="May 18, 2026",
    export_format="PDF"
    )

    # ✅ AGAIN close popup
    dashboard_page.page.keyboard.press("Escape")

@pytest.mark.sanity
def test_dropdown_bam(login_wims_application):
   dashboard_page = DashboardPage(login_wims_application)
   dashboard_page.navigate_to_management_overview()
   dashboard_page.verify_sites_in_bam(["KWD"])

@pytest.mark.sanity
def test_site_properties_export(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_management_overview()

    excel_download = dashboard_page.export_site_properties_excel()
    assert excel_download is not None
    assert excel_download.suggested_filename.lower().endswith((".xls", ".xlsx"))

    pdf_download = dashboard_page.export_site_properties_pdf()
    assert pdf_download is not None
    assert pdf_download.suggested_filename.lower().endswith(".pdf")

@pytest.mark.sanity
def test_monthly_alarms(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_management_overview()
    dashboard_page.verify_monthly_alarm_filters(6)
    dashboard_page.verify_monthly_alarm_filters(12)
    # dashboard_page.verify_monthly_alarm_filters(18)


@pytest.mark.sanity
def test_weekly_alarms(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_management_overview()
    # dashboard_page.verify_weekly_alarm_filters(2)
    dashboard_page.verify_weekly_alarm_filters(4)
    dashboard_page.verify_weekly_alarm_filters(6)
    dashboard_page.verify_weekly_alarm_filters(8)
################## Management Overview Page End #######################

################## Rolling Stock Monitoring Page Start #######################
@pytest.mark.sanity
def test_dashboard_navigation(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_rolling_stock_monitoring()
    dashboard_page.verify_rolling_stock_monitoring()


@pytest.mark.sanity
def test_train_alarm_alert_list_table(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_rolling_stock_monitoring()
    dashboard_page.verify_train_alarm_alert_list_table()


@pytest.mark.sanity
def test_monitoring_list_table(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_rolling_stock_monitoring()
    dashboard_page.verify_monitoring_list_table()

@pytest.mark.sanity
def test_verify_wims_status_visibility_and_tooltips(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_rolling_stock_monitoring()
    dashboard_page.verify_wims_status_header_visible()
    dashboard_page.verify_available_wims_status_items_visible()
    dashboard_page.verify_wims_processing_tooltip()
    dashboard_page.verify_oss_connectivity_tooltip()
    dashboard_page.verify_equip_connectivity_tooltip()

################## Rolling Stock Monitoring Page End #######################

################## system-health-monitoring - dashboard Start ################
@pytest.mark.sanity
def test_wayside_system_health_summary(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_system_health_dashboard()
    dashboard_page.verify_wayside_system_health(['BCR'])

@pytest.mark.sanity
def test_wayside_system_health_detailed(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_system_health_dashboard()
    dashboard_page.verify_wayside_system_health_detailed(['BCR'])

@pytest.mark.sanity
def test_av_report(login_wims_application):
    """Verify the AV Report opens"""
    """Verify toggle works and then AV Report opens (Dashboard should open only once)"""
    dashboard_page = DashboardPage(login_wims_application)
    # Navigate ONLY ONCE
    dashboard_page.navigate_to_system_health_dashboard()
    # Step 2: Click AV Report
    dashboard_page.click_av_report()

@pytest.mark.sanity
def test_system_faults_dashboard(login_wims_application):
    """Verify that System Faults Dashboard loads successfully"""
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_system_faults()
    dashboard_page.verify_system_faults_loaded()

################## system-health-monitoring - dashboard End ################

################## Weather Monitoring Page Start ###########################

@pytest.mark.sanity
def test_weather_monitoring(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    dashboard_page.navigate_to_weather_monitoring()
    dashboard_page.verify_weather_monitoring()

@pytest.mark.sanity
def test_weather_station_status_table(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    #  Navigate to Weather Monitoring page
    dashboard_page.navigate_to_weather_monitoring()
    # Verify table exists
    dashboard_page.verify_weather_station_status_table()

@pytest.mark.sanity
def test_weather_data_table(login_wims_application):
    dashboard_page = DashboardPage(login_wims_application)
    # Navigate to Weather Monitoring
    dashboard_page.navigate_to_weather_monitoring()
    # Verify table exists
    dashboard_page.verify_weather_data_table()

################## Weather Monitoring Page End ###########################