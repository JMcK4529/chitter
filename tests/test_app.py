from playwright.sync_api import Page, expect
import pytest, os

def test_get_index(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    # Go to index page (not logged in)
    page.goto(f"http://{test_web_address}/")
    # Compare all div tags with the classes expected of them
    div_list = page.locator("div")
    class_list = [
        "container", "column", "login-prompt", 
        "column", "peep", "column"
    ]
    for div, class_label in zip(div_list.all(), class_list):
        expect(div).to_have_class(class_label)
    # Check each peep-related div by class for expected contents
    peeps = page.locator(".peep")
    expect(peeps).to_have_id("1")
    timestamps = page.locator(".timestamp")
    expect(timestamps).to_have_text("2023-12-07 11:13:15")
    contents = page.locator(".content")
    expect(contents).to_have_text("Welcome to Chitter!")
    by_users = page.locator(".by-user")
    expect(by_users).to_have_text("JMcK4529")

def test_get_login(db_connection, page, test_web_address):
    """
    Tests for:
    Title = login to chitter
    No error div class for standard get method
    Three inputs: text, password, submit
    """
    db_connection.seed("seeds/chitter.sql")
    # Go to login page and check its title
    page.goto(f"http://{test_web_address}/login")
    expect(page).to_have_title("Login to Chitter!")
    # Check that there are no errors on initial load
    div_list = page.locator("div").all()
    assert all(".error" not in div.get_attribute("class") 
               for div in div_list)
    # Check that the expected input fields are present
    input_list = page.locator("input").all()
    expected_input_types = ["text", "password", "submit"]
    for input, expected in zip(input_list, expected_input_types):
        expect(input).to_have_attribute("type", expected)

def test_index_checks_for_session(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    # Go to index page (not logged in)
    page.goto(f"http://{test_web_address}/")
    # Check if the login-prompt appears on page
    div_list = page.locator("div").all()
    assert any("login-prompt" in div.get_attribute("class") 
               for div in div_list)
    # Fill in the login form with a nonexistent user
    page.get_by_label("Username").fill("NonUser")
    page.get_by_label("Password").fill("FakePassword")
    page.get_by_role("button").click()
    # Check for redirect to login page
    expect(page).to_have_url(f"http://{test_web_address}/login")
    # Login with test/creator account, starting a session
    page.get_by_label("Username").fill("JMcK4529")
    page.get_by_label("Password").fill(os.getenv('CREATOR_PASS'))
    page.get_by_role("button").click()
    # Check for redirect to index page without login prompt
    expect(page).to_have_url(f"http://{test_web_address}/")
    div_list = page.locator("div").all()
    assert all("login-prompt" not in div.get_attribute("class") 
               for div in div_list)

def test_post_login(db_connection, page, test_web_address):
    """
    Go to /login
    Fill in form badly
    Submit
    Check for reload
    Fill in form correctly
    Submit
    Check for redirect to /
    """
    db_connection.seed("seeds/chitter.sql")
    # Go to login page
    page.goto(f"http://{test_web_address}/login")
    # Fill in form with non-existent user details
    page.get_by_label("Username").fill("NonUser")
    page.get_by_label("Password").fill("FakePassword")
    page.get_by_role("button").click()
    # Check there is no redirection
    expect(page).to_have_url(f"http://{test_web_address}/login")
    # Check there is an error div with the expected text
    error_div = page.locator(".error")
    expect(error_div).to_have_text("Username or password was incorrect.")
    # Fill the form with test/creator details
    page.get_by_label("Username").fill("JMcK4529")
    page.get_by_label("Password").fill(os.getenv('CREATOR_PASS'))
    page.get_by_role("button").click()
    # Check for redirect to index page with username displayed
    expect(page).to_have_url(f"http://{test_web_address}/")
    assert "JMcK4529" in page.locator("#column1").inner_text()

def test_logout(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    # Go to login page
    page.goto(f"http://{test_web_address}/login")
    # Sign in as test/creator
    page.get_by_label("Username").fill("JMcK4529")
    page.get_by_label("Password").fill(os.getenv('CREATOR_PASS'))
    page.get_by_role("button").click()
    # Check for redirect to index page with username displayed
    expect(page).to_have_url(f"http://{test_web_address}/")
    assert any("JMcK4529" in div.inner_text() 
               for div in page.locator("div").all())
    # Click Logout
    page.get_by_role("button").click()
    # Check for redirect to index page without user-details div
    expect(page).to_have_url(f"http://{test_web_address}/")
    print([div.get_attribute("class") for div in page.locator("div").all()])
    assert all("user-details" not in div.get_attribute("class") 
               for div in page.locator("div").all())

#@pytest.mark.skip(reason="Not yet implemented.")
def test_get_signup(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    # Go to signup page
    page.goto(f"http://{test_web_address}/signup")
    # Check for expected inputs within form
    inputs = page.locator("input").all()
    names = ["Email", "Username", "Password", "Verify"]
    for input, name in zip(inputs[:-1], names):
        expect(input).to_have_attribute("name", name)
    expect(inputs[-1]).to_have_attribute("type", "submit")

@pytest.mark.skip(reason="Not yet implemented.")
def test_post_signup(db_connection, page, test_web_address):
    stuff=None