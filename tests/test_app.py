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
    for input in page.locator("input").all():
        print(input.get_attribute("name"))
    [input.click() for input in page.locator("input").all() if input.get_attribute("name") == "login"]
    # Check for redirect to index page with username displayed
    expect(page).to_have_url(f"http://{test_web_address}/")
    assert any("JMcK4529" in div.inner_text() 
               for div in page.locator("div").all())
    # Click Logout
    [input.click() for input in page.locator("input").all() if input.get_attribute("name") == "logout"]
    # Check for redirect to index page without user-details div
    expect(page).to_have_url(f"http://{test_web_address}/")
    print([div.get_attribute("class") for div in page.locator("div").all()])
    assert all("user-details" not in div.get_attribute("class") 
               for div in page.locator("div").all())

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

def test_post_signup(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    # Go to signup page
    page.goto(f"http://{test_web_address}/signup")

    # Attempt signup with empty fields
    page.get_by_label("Email").fill("")
    page.get_by_label("Username").fill("")
    page.get_by_label("Password", exact=True).fill("NewPassword")
    page.get_by_label("Verify Password").fill("NewPassword")
    page.get_by_role("button").click()
    # Expect template render with error div
    error_text = "Username can't be empty."
    assert any(error_text in div.inner_text()
               for div in page.locator("div").all()
               if div.get_attribute("class") == "error")
    
    # Attempt signup with empty fields except username
    page.get_by_label("Email").fill("")
    page.get_by_label("Username").fill("NewUsername")
    page.get_by_label("Password", exact=True).fill("NewPassword")
    page.get_by_label("Verify Password").fill("NewPassword")
    page.get_by_role("button").click()
    # Expect template render with error div
    error_text = "Email can't be empty."
    assert any(error_text in div.inner_text()
               for div in page.locator("div").all()
               if div.get_attribute("class") == "error")
    
    # Attempt signup with empty fields except username
    page.get_by_label("Email").fill("NewEmail@test.com")
    page.get_by_label("Username").fill("NewUsername")
    page.get_by_label("Password", exact=True).fill("")
    page.get_by_label("Verify Password").fill("")
    page.get_by_role("button").click()
    # Expect template render with error div
    error_text = "Password must contain at least 8 characters."
    assert any(error_text in div.inner_text()
               for div in page.locator("div").all()
               if div.get_attribute("class") == "error")

    # Attempt signup with all test/creator details
    page.get_by_label("Email").fill("test@mail.co.uk")
    page.get_by_label("Username").fill("JMcK4529")
    page.get_by_label("Password", exact=True).fill(os.getenv('CREATOR_PASS'))
    page.get_by_label("Verify Password").fill(os.getenv('CREATOR_PASS'))
    page.get_by_role("button").click()
    # Expect template render with error div
    error_text = "Email address already has an associated account."
    assert any(error_text in div.inner_text()
               for div in page.locator("div").all()
               if div.get_attribute("class") == "error")
    
    # Attempt signup with test/creator email, different otherwise
    page.get_by_label("Email").fill("test@mail.co.uk")
    page.get_by_label("Username").fill("NewUsername")
    page.get_by_label("Password", exact=True).fill("NewPassword")
    page.get_by_label("Verify Password").fill("NewPassword")
    page.get_by_role("button").click()
    # Expect template render with error div
    error_text = "Email address already has an associated account."
    assert any(error_text in div.inner_text()
               for div in page.locator("div").all()
               if div.get_attribute("class") == "error")
    
    # Attempt signup with test/creator username, different otherwise
    page.get_by_label("Email").fill("NewEmail@test.com")
    page.get_by_label("Username").fill("JMcK4529")
    page.get_by_label("Password", exact=True).fill("NewPassword")
    page.get_by_label("Verify Password").fill("NewPassword")
    page.get_by_role("button").click()
    # Expect template render with error div
    error_text = "Username is already in use."
    assert any(error_text in div.inner_text()
               for div in page.locator("div").all()
               if div.get_attribute("class") == "error")
    
    # Attempt signup with unused email and username, mismatched passwords
    page.get_by_label("Email").fill("NewEmail@test.com")
    page.get_by_label("Username").fill("NewUsername")
    page.get_by_label("Password", exact=True).fill("NewPassword1")
    page.get_by_label("Verify Password").fill("NewPassword2")
    page.get_by_role("button").click()
    # Expect template render with error div
    error_text = "Passwords did not match."
    assert any(error_text in div.inner_text()
               for div in page.locator("div").all()
               if div.get_attribute("class") == "error")
    
    # Signup with unused email and username, correctly verified password
    page.get_by_label("Email").fill("NewEmail@test.com")
    page.get_by_label("Username").fill("NewUsername")
    page.get_by_label("Password", exact=True).fill("NewPassword")
    page.get_by_label("Verify Password").fill("NewPassword")
    page.get_by_role("button").click()
    # Expect index page with NewUsername displayed
    expect(page).to_have_url(f"http://{test_web_address}/")
    assert any(div.get_attribute("class") == "user-details"
               for div in page.locator("div").all())

def test_post_peep_post(db_connection, page, test_web_address):
    db_connection.seed("seeds/chitter.sql")
    # Go to signup page
    page.goto(f"http://{test_web_address}/signup")
    # Sign up as a new user
    page.get_by_label("Email").fill("testuser@test.co.uk")
    page.get_by_label("Username").fill("TestUsername")
    page.get_by_label("Password", exact=True).fill("TestPassword")
    page.get_by_label("Verify Password").fill("TestPassword")
    page.get_by_role("button").click()
    # Check for redirect to index page (logged in)
    expect(page).to_have_url(f"http://{test_web_address}/")
    assert any(div.get_attribute("class") == "user-details"
               for div in page.locator("div").all())
    # Fill in peep_post form and submit
    page.get_by_label("Type your peep here!").fill("This is my new test peep!")
    [input.click() for input in page.locator("input").all() if input.get_attribute("name") == "submit-peep"]
    # Check that the new peep appears above the old one
    div_tags = page.locator("div").all()
    ids = []
    for div in div_tags:
        try:
            if div.get_attribute("class") == "peep":
                ids.append((div_tags.index(div), int(div.get_attribute("id"))))
        except:
            pass
    assert ids[0][1] > ids[1][1]