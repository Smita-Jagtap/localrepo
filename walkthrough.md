# Test Automation Framework Setup Walkthrough

The framework has been generated directly in `c:\GitLab_DUO\WIMS_Sanity_Automation` with the following components and sample Python code:

### Configuration (`config/`)
- **`settings.py`**: Global settings such as timeouts and directory paths.
- **`environment.py`**: Environment management logic (dev/qa/prod) for dynamic base URLs.
- **`test_data.json`**: Sample JSON data loaded directly into the fixtures.

### Page Object Models (`pages/`)
- **`base_page.py`**: Shared Playwright actions like `navigate()`, `wait_for_load_state()`.
- **`login_page.py`**, **`dashboard_page.py`**, **`user_profile_page.py`**, **`settings_page.py`**: Locators and action wrapper functions structured following the Page Object Model pattern.

### Testing Base (`tests/` and `utils/`)
- **`utils/`**: Reusable wait helpers, data helpers, and a screenshot handler utility for failed tests.
- **`tests/conftest.py`**: Contains test fixtures, logging initialization, and test hooks to automatically screenshot on failure.
- **`test_login.py`**, **`test_dashboard.py`**, **`test_user_profile.py`**, **`test_settings.py`**: Skeleton test scenarios for the major workflows using fixtures and POMs.

### Root Files
- **`requirements.txt`**: Declares dependencies (`pytest`, `playwright`, `pytest-html`).
- **`pytest.ini`**: Registers `sanity` marks, CLI logging configs, and specifies the test report format structure.
- **`README.md`**: Provides straightforward execution commands (`pytest -m sanity`).
- Supported directories `logs/` and `reports/` have been placed correctly to organize outputs.
