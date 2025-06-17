import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Run without opening a browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Step 1: Open Brella Login Page
driver.get("https://satellite.brella.io/login")
time.sleep(3)

# Step 2: Enter Email
email_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))
email_input.send_keys("Replace with actual email")  # Replace with actual email

# Click 'Continue with email'
continue_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-test="submit-button"]')))
continue_button.click()

# Step 3: Enter Password
password_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//input[@data-test="password-input"]')))
password_input.send_keys("Replace with actual password")  # Replace with actual password

# Click 'Sign in'
login_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-test="submit-button"]')))
login_button.click()

# Step 4: Wait for redirect & go to attendee page
WebDriverWait(driver, 15).until(EC.url_changes("https://satellite.brella.io/login"))
driver.get("https://satellite.brella.io/events/SATShow25/people")
time.sleep(3)  # Allow page to load

# Step 5: Click "All Attendees" Button
try:
    all_attendees_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-test="attendee-list-tabs-attendees"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView();", all_attendees_button)
    time.sleep(1)  # Small delay
    driver.execute_script("arguments[0].click();", all_attendees_button)
    print("✅ Clicked 'All Attendees' tab successfully!")
    time.sleep(3)  # Allow attendees to load
except Exception as e:
    print("❌ Error: Could not find or click 'All Attendees' button:", e)

# Step 6: Scrape Attendee Data for 983 Pages
attendee_data = []

for page in range(1, 993):  # Loop through 983 pages
    print(f"🔄 Scraping page {page}...")

    # Store old list of attendee names before clicking Next
    old_attendee_names = [a.text.strip() for a in driver.find_elements(By.XPATH, '//h2[@data-test="attendee-card-name"]')]

    # Scrape the current attendee list
    attendees = driver.find_elements(By.XPATH, '//div[contains(@data-test, "profile-card")]')

    for attendee in attendees:
        try:
            name = attendee.find_element(By.XPATH, './/h2[@data-test="attendee-card-name"]').text.strip()
        except:
            name = "N/A"

        # ✅ Extract "Title & Company" correctly
        try:
            title_element = WebDriverWait(attendee, 2).until(
                EC.presence_of_element_located((By.XPATH, './/p[contains(@class, "css-1gr96e6")]'))
            )
            raw_title = title_element.text.strip()
        except:
            try:
                title_element = attendee.find_element(By.XPATH, './/p')
                raw_title = title_element.text.strip()
            except:
                raw_title = "N/A"

        # ✅ Normalize and clean separators
        raw_title = raw_title.replace("âˆ™", "•").replace("∙", "•").replace("Â", "").replace("\n", " • ")

        # ✅ Extract "Title" & "Company" using regex
        match = re.match(r"^(.*)\s•\s(.*?)$", raw_title)
        if match:
            title, company = match.groups()
        else:
            title = raw_title.strip()
            company = "N/A"  # If no company is detected

        try:
            persona = attendee.find_element(By.XPATH, './/span[@data-test="attendee-card-persona"]').text.strip()
        except:
            persona = "N/A"

        try:
            description = attendee.find_element(By.XPATH, './/p[@data-test="attendee-pitch"]').text.strip()
        except:
            description = "N/A"

        # Save data
        attendee_data.append({"Name": name, "Title": title, "Company": company, "Persona": persona, "Description": description})
        print(f"✅ Scraped: {name} - {title} | {company}")

    # Step 7: Click "Next Page" Button (Scroll & Click)
    try:
        # Find all pagination buttons
        pagination_buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "ant-pagination-item-link")]')

        # If multiple buttons exist, get the last one (usually the "Next" button)
        next_button = pagination_buttons[-1] if pagination_buttons else None

        if next_button:
            print(f"🔎 Found 'Next Page' button: {next_button.get_attribute('outerHTML')}")
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)  # Small delay
            driver.execute_script("arguments[0].click();", next_button)
            print(f"➡️ Clicked 'Next' to page {page + 1}")

            # ✅ Wait for a new attendee name to appear (ensures new page is loaded)
            WebDriverWait(driver, 10).until(
                lambda d: any(a.text.strip() not in old_attendee_names for a in d.find_elements(By.XPATH, '//h2[@data-test="attendee-card-name"]'))
            )
            time.sleep(3)  # Allow next page to load

        else:
            print("❌ No 'Next Page' button found.")
            break
    except Exception as e:
        print("⚠️ No more pages to scrape or could not click 'Next Page' button:", e)
        break  # Stop if no more pages

# Step 8: Save Scraped Data to CSV
df = pd.DataFrame(attendee_data)
df.to_csv("attendees_data.csv", index=False)

print("✅ Scraping complete! Data saved to attendees_data.csv.")

# Close browser
driver.quit()
