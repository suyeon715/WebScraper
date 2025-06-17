# WebScraper

This project automates the scraping of attendee information from the SATShow25 event on satellite.brella.io. It uses Selenium WebDriver to log in, navigate the UI, paginate through over 980 pages of profiles, and extract key details into a structured .csv file.

🚀 Features
Automated login via email and password

Click-through to the "All Attendees" tab

Robust handling of pagination (up to 990+ pages)

Extracts attendee:

Name

Title

Company (parsed from title line)

Persona

Personal description

Cleans and normalizes encoded separators (e.g. âˆ™, ∙, •)

Saves data to attendees_data.csv

📁 Output Format
The resulting CSV includes the following columns:

Name	Title	Company	Persona	Description
Jane Smith	Head of Strategy	OrbitNow Inc.	Aerospace Innovator	"Passionate about satellite compute"
John Doe	Investment Associate	Sky VC	Investor	"Looking for early-stage startups"
...	...	...	...	...

⚙️ Setup Instructions
Prerequisites
Python 3.8+

Google Chrome installed

Install Dependencies
bash
Copy
Edit
pip install selenium pandas webdriver-manager
▶️ How to Run
Open brella_scraper.py

Replace the email and password fields with your own credentials:

python
Copy
Edit
email_input.send_keys("your_email@example.com")
password_input.send_keys("your_password")
Run the script:

bash
Copy
Edit
python brella_scraper.py
The script will navigate through the site and save a CSV:

Copy
Edit
attendees_data.csv
🔐 Security Warning
❗ Your Brella credentials are currently hard-coded in the script. To keep them secure:

Use environment variables or a .env file

Do not commit sensitive credentials to version control

🧠 Logic Behind Title & Company Parsing
Some attendees list both title and company in one string, separated by characters like:

• or ∙ (e.g. "Senior Associate • Space Capital")

- or newlines (\n)

This scraper uses regex to split at the last known separator, ensuring:

"Senior Associate - Constellation Team • Space Capital"
→ Title = "Senior Associate - Constellation Team"
→ Company = "Space Capital"

📌 Limitations
Requires Chrome and internet access

Subject to page structure changes by Brella

Respects Brella's login system and session cookies

Not parallelized — runs single-threaded for safety

📄 License
This project is for internal use. Please ensure scraping is compliant with Brella’s Terms of Service and your organization’s data use policies.

Let me know if you'd like to add features like:

Headed/visible mode (for debugging)

Grata or PitchBook enrichment

Classification by investor types or funding size

Happy scraping! 🚀
