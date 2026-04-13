import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright

# ========================================================================
# PYTEST + PLAYWRIGHT TEST CONFIGURATION FILE
# ========================================================================
# This file provides:
# 1. Command-line options (browser, base URL, video, screenshots, etc.)
# 2. Hooks to track test results
# 3. Fixtures for browser setup and teardown
# 4. Screenshot, video, and trace attachments to Allure reports
# ========================================================================

# ----------------------------------------------------------------------------
# STEP 1: ADD COMMAND LINE OPTIONS OR TERMINAL OPTIONS TO THE "parser"
# ----------------------------------------------------------------------------
def pytest_addoption(parser):
    '''
    Let's say I pass some parameters in terminal while running pytest like :
        pytest  test.py --headed --browser chromium --base-url "url"
    These parameters will be received by this "parser" object in the argument.
    So This is the 1st function , and it will add terminal values to the parser.
    '''

    """
    By using this parser, we have a method called "addoption" and what this addoption will do ?
        It Adds command line options for test configuration.
        Suppose we are not passing params in terminal then we can override these
        when running pytest or store defaults in pytest.ini file.
    """
    parser.addoption("--browser", default="chromium", help="Browser: chromium, firefox, webkit")
    parser.addoption("--headed", action="store_true", help="Run in headed (visible) mode")
    parser.addoption("--base-url", default="https://tutorialsninja.com/demo/", help="Base URL for tests")
    parser.addoption("--video", default="retain-on-failure", help="Record video: on, off, retain-on-failure")
    parser.addoption("--screenshot", default="only-on-failure", help="Take screenshot: on, off, only-on-failure")
    parser.addoption("--tracing", default="retain-on-failure", help="Tracing: on, off, retain-on-failure")

# ----------------------------------------------------------------------------
# STEP 2: GET CONFIGURATION VALUES from (CMDLINE/TERMINAL OR pytest.ini)
# ----------------------------------------------------------------------------
def get_config_value(config, option_name):
    '''
    the above function "pytest_addoption", adds terminal options to the parser.
    But here, it will read those options like 'what browser, base-url we have passed',
        'which video and screenshot options we have passed'. So the option values will be read
        by this "get_config_value" function.
    If terminal values are not available, then this function will read from "pytest.ini" file.
    This is a reusable function and we will call from another fixture method.
    '''

    """
    Helper to read configuration values.
    Tries to get from command line first, otherwise from pytest.ini.
    Supports both string and boolean options.
    """
    # Try command-line first
    cmd_value = config.getoption(option_name)
    if cmd_value is not None:
        return cmd_value

    # Fallback to pytest.ini
    if option_name == "headed":
        ini_value = config.getini(option_name)
        return ini_value.lower() == "true" if isinstance(ini_value, str) else ini_value
    else:
        return config.getini(option_name)


# ----------------------------------------------------------------------------
# STEP 3: HOOK TO TRACK/CAPTURE THE TEST RESULTS (PASS/FAIL)
# ----------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    Whenever we specify this decorator "@pytest.hookimpl", this will actually capture the results of the test.
    It will take a parameter as "hookwrapper" and function name is also fixed "pytest_runtest_makereport".
    "call" is optional, it actually comes in API part.
    '''

    """
    What this function will do ?
        This will Captures the test result (pass or fail or skip) after each test run.
        Once it captures the test results, based on that result, later we will capture 
            the screenshot, video and trace. 
        And later this is used to decide whether to take screenshots or save traces.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

# ----------------------------------------------------------------------------
# STEP 4: FIXTURE 1 - BROWSER CONTEXT SETUP
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def browser_context(request):
    '''
    This is the main fixture that controls everything. page, browser, Playwright instance, context etc.
    It takes a parameter "request"
    '''

    """
    Creates and manages the Playwright browser context.
    - Reads configuration (browser, headed mode, video settings)
    - Starts the Playwright browser
    - Enables video recording if configured
    - Cleans up automatically after each test
    """

    # Read configuration values
    '''
    This will read the configuration values. In 1st function "pytest_addoption" we have 
        already added these options. If not passed in terminal, options are available in pytest.ini file.
    Initially when we start the test the things needed are : browser name, headed or headless mode, also 
        take video_option as at the time of creating context we specify video location.
    '''
    browser_name = get_config_value(request.config, "browser")
    headed_flag = get_config_value(request.config, "headed")
    video_option = get_config_value(request.config, "video")

    print(f"🎯 Starting browser: {browser_name}")
    print(f"🎯 Headless mode: {not headed_flag} (headed={headed_flag})")


    # Start Playwright
    '''
    By taking the configuration value, we will initiate playwright instance.
    Here We will create our own PW fixture, page instance, context everything.
    To create a playwright instance we have to use "sync_playwright()" function and
        this is available in 'from playwright.sync_api import sync_playwright'.
    Once we start the playwright instance we are storing it in 'playwright' object.
    '''
    playwright = sync_playwright().start()


    # Launch the specified browser
    '''
    Now here we will decide the browser. This particular piece of code will decide 
        the browser and return the browser here.
    We could have used "browser = playwright.chromium.launch(headless=False)", but then
        we need to come here and change everytime to True/False. That's why we have used 
        "headless=not headed_flag".
        The "headed_flag" value comes from "pytest_addoption" function or pytest.ini file.
    '''
    if browser_name.lower() == "chromium":
        browser = playwright.chromium.launch(headless=not headed_flag)
    elif browser_name.lower() == "firefox":
        browser = playwright.firefox.launch(headless=not headed_flag)
    elif browser_name.lower() == "webkit":
        browser = playwright.webkit.launch(headless=not headed_flag)
    else:
        raise ValueError(f"❌ Unsupported browser: {browser_name}")


    # Create a browser context (optionally with video recording)
    '''
    Once we have created the browser, we need to create a context. Because through the context
        we can control videos, screeshots and trace.
    We are specifying the "record_video_dir" record video location, as we can only specify the
        location of video only while creating context.Suppose "video_option" is off then we dont
        need to specify any location.
    '''
    if video_option in ["on", "retain-on-failure"]:
        context = browser.new_context(record_video_dir="reports/videos")
    else:
        context = browser.new_context()


    # Yield the context for use in tests
    '''
    After context gets created, finally it will return the context. 
    If we want the fixture to return some value then we need to put "yield context". Here context
        will be returned along with the yield.
    But still we have'nt created the page, as the Hirarchy says "PW fixture --> browser --> context --> page".
    Fore page we have to create a separate fixture where we need to use this browser_context .
    '''
    yield context

    # Clean up after the test
    print("🧹 Closing browser context and stopping Playwright...")
    context.close()
    browser.close()
    playwright.stop()


# ----------------------------------------------------------------------------
# STEP 5: FIXTURE 2 - PAGE CREATION AND TEST ARTIFACT MANAGEMENT
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def page(request, browser_context):
    '''
    We are creating our own page fixture, not the existing Playwright page fixture.
    To create page, we need the context. The context we are getting from the previous fixture
        "browser_context" and we are calling the fixture function in the argument of this fixture.
        "request" is another parameter we need to pass.

    '''

    """
    Creates a new browser page for each test.
    - Navigates to the base URL
    - Starts tracing (if enabled)
    - Captures screenshots, traces, and videos for failed tests
    - Attaches all artifacts to Allure report
    """

    # Read test configuration
    '''
    Here as fixture 1, we read the configuration values form the pytest.ini file or 
        the terminal. As the time of launching the page, we need this parameter.
    '''
    base_url = get_config_value(request.config, "base_url")
    screenshot_option = get_config_value(request.config, "screenshot")
    tracing_option = get_config_value(request.config, "tracing")
    video_option = get_config_value(request.config, "video")

    print(f"🌐 Navigating to: {base_url}")

    # Start tracing if tracing_option is enabled
    '''
    We can configure the trace through pytest.ini file or through context. But in framework
        we will be using both that's why we have "--tracing=retain-on-failure" in .ini file
        and also "screenshots=True, snapshots=True, sources=True" in context.
    '''
    if tracing_option in ["on", "retain-on-failure"]:
        print("📹 Tracing enabled - capturing screenshots and actions")
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True) # starting the trace

    # Create and navigate to base URL
    '''
    Now we are creating a new page using the browser_context that is yield from the fixture1 function.
    And by using this page, we are going to launch the URL.
    '''
    page = browser_context.new_page()
    page.goto(base_url)

    # Yield the page to the test
    '''
    Now once the page is got created, we are returning the page for the tests. This page
        we are going to use in our test cases.
    '''
    yield page

    # ------------------------------------------------------------------------
    # After the test: manage artifacts (screenshots, videos, traces)
    # ------------------------------------------------------------------------
    '''
    All the below reporting managements will be done after the execution is completed, that's why
        we are these are kept after the yield and after returning the page.
    We need to capture the test name, and if its a failed test, then also we need to capture
        the failed test information. And print the information
    '''
    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    print(f"📊 Test '{test_name}' result: {'❌ FAILED' if test_failed else '✅ PASSED'}")

    # Save and attach trace
    '''
    Finally we need to make sure the trace file, videos, screenshots should be part of the
        report.
    If tracing is "on" or "retain-on-failure" we take the path of the trace.
    We are stoping the trace and passing the path of the trace. 
    '''
    if tracing_option in ["on", "retain-on-failure"]:
        trace_path = f"reports/traces/{test_name}_trace.zip"
        browser_context.tracing.stop(path=trace_path) # Here we are stoping the trace
        print(f"💾 Trace saved: {trace_path}")

        # Attach trace to Allure report if test failed
        # Currently ZIP file is not supporting to attach in allure reports
        '''
        Even though we have the trace file, we cant attach it in allure report, as
            allure report does'nt support .zip file attachment. 
            That's why its commented out, in future if its supported we can use this.
        '''
        # if test_failed:
        #     allure.attach.file(
        #         trace_path,
        #         name=f"{test_name}_trace",
        #         attachment_type=allure.attachment_type.ZIP
        #     )
        #     print("📎 Trace attached to Allure report")

    # Take screenshot if test failed
    '''
    But screenshots we can attach to the allure report.
    '''
    if test_failed and screenshot_option in ["on", "only-on-failure"]:
        screenshot_path = f"reports/screenshots/{test_name}.png"
        page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")

        # Attach to Allure report
        allure.attach.file(
            screenshot_path,
            name=f"{test_name}_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        print("📎 Screenshot attached to Allure report")


    # Attach video if available and test failed
    '''
    Also we can attach the video to the allure report.
    '''
    if test_failed and video_option in ["on", "retain-on-failure"]:
        video_path = page.video.path() if page.video else None

        if video_path and Path(video_path).exists():
            # Attach to Allure report
            allure.attach.file(
                video_path,
                name=f"{test_name}_video",
                attachment_type=allure.attachment_type.WEBM
            )
        print("🎥 Video attached to Allure report")



'''
Explain the conftest.py framework that you use ?

    "pytest_addoption()" : 1st method will add terminal options or pytest.ini options to parser
    
    get_config_value() : 2nd method will read those options.
    
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport() : 3rd method will return the results of the tests, passed/failed/skipped.
    
    @pytest.fixture(scope="function")
    def browser_context() : 4th method will create the Browser context and it will return the browser context.
    
    @pytest.fixture(scope="function")
    def page : 5th method will create our own page fixture using the same Browser context.
        at the time of creating the page, we are using base_url, screenshot_option, tracing_option,
        and video_option.
        And Finally we are attaching the screenshots and videos to the allure report and only saving
        the trace.zip file as we can't attach the .zip file to the allure report.

'''