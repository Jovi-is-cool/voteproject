Try AI directly in your favorite apps … Use Gemini to generate drafts and refine content, plus get Gemini Pro with access to Google's next-gen AI for $19.99 $6.49 for 3 months
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# This helps us see immediately if the script has actually started
print("--------------------------------------------------")
print("DEBUG: Script is starting... if you see this, Python is working.")
print("--------------------------------------------------")

def run_counter_bot(poll_id, athlete_name, total_runs=100):
    # Modern device profiles to rotate through to look like different people
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
    ]

    direct_poll_url = f"https://poll.fm/{poll_id}"
    successful_votes = 0

    print(f"Targeting Poll ID: {poll_id}")
    print(f"Goal: {total_runs} successful votes")

    for i in range(total_runs):
        print(f"\n[Run #{i+1} of {total_runs}] Initializing Stealth Browser...")

        chrome_options = Options()

        # 1. Randomized User Agent
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

        # 2. Critical Stealth Flags
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Block images to keep it fast
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        driver = None
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Remove the 'webdriver' flag
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            print(f"Navigating to: {direct_poll_url}")
            driver.get(direct_poll_url)

            wait = WebDriverWait(driver, 20)

            # Find the Name
            print(f"Searching for '{athlete_name}'...")
            xpath = f"//span[contains(text(), '{athlete_name}')] | //label[contains(text(), '{athlete_name}')]"
            name_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Human-like Mouse Movement
            actions = ActionChains(driver)
            actions.move_to_element(name_element).perform()
            time.sleep(random.uniform(1.0, 2.5))
            name_element.click()
            print(f"Selected: {athlete_name}")

            # "Thinking" Delay
            think_time = random.uniform(3.0, 6.0)
            print(f"Waiting {think_time:.1f}s to look human...")
            time.sleep(think_time)

            # Click Vote
            vote_btn_selector = f"#pd-vote-button{poll_id}, .pds-vote-button"
            vote_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, vote_btn_selector)))

            actions.move_to_element(vote_btn).perform()
            time.sleep(0.5)
            vote_btn.click()
            print("Vote submitted! Waiting for server confirmation...")

            # 6. Verify Results Page
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pds-results-list")))
            print(f"SUCCESS: Vote #{i+1} verified and recorded.")
            successful_votes += 1

            # Wait on results page to simulate reading results
            time.sleep(random.uniform(4, 8))

        except Exception as e:
            print(f"ERROR on Run #{i+1}: {str(e)[:100]}...")

        finally:
            if driver:
                try:
                    driver.quit()
                    print(f"Session #{i+1} closed.")
                except:
                    pass

        # Add a delay between runs so the IP/Session doesn't look spammy
        if i < total_runs - 1:
            cooldown = random.randint(10, 20)
            print(f"Waiting {cooldown} seconds before starting the next run...")
            time.sleep(cooldown)

    print("\n==================================================")
    print(f"Finished! Total Verified Votes: {successful_votes}/{total_runs}")
    print("==================================================")

if __name__ == "__main__":
    # Kaine Boone's Poll Details
    POLL_ID = "16476108"
    TARGET_NAME = "Kaine Boone"

    # Set to 5 runs as requested
    run_counter_bot(POLL_ID, TARGET_NAME, total_runs=100)
