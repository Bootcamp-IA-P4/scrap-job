import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CompanyNameCleaner:
    """Cleans and standardizes company names."""

    @staticmethod
    def clean_company_name(company_name):
        """
        Cleans and standardizes the company name.
        """
        company_name = company_name.replace(".", "").replace(",", "").replace(" & ", "-").lower().replace(" ", "-")
        company_name = company_name.replace("ñ", "n")  # Replace 'ñ' with 'n'
        company_name = re.sub(r'[()]', '', company_name)
        company_name = re.sub(r'\-sau$', '-sa', company_name)
        company_name = re.sub(r'\-slu$', '-sl', company_name)
        company_name = re.sub(r'\-sociedad\-anonima.*$', '-sa', company_name, flags=re.IGNORECASE)
        company_name = re.sub(r'\-sociedad\-limitada.*$', '-sl', company_name, flags=re.IGNORECASE)
        return company_name


class WebScraper:
    """Handles web interactions using Selenium."""

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def accept_cookies(self):
        """Accepts cookies on the website."""
        try:
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "didomi-notice-agree-button"))
            )
            submit_button.click()
            print("Agree and close clicked.")
        except Exception as e:
            print(f"Error: {e} - Agree button not found or already clicked.")

    def get_company_data(self, url):
        """Extracts company names and URLs from the ranking table."""
        self.driver.get(url)
        time.sleep(5)
        company_data = []

        try:
            table = self.driver.find_element(By.ID, "tabla-ranking")
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 3:
                    continue
                company_cell = cells[2]
                try:
                    company_link = company_cell.find_element(By.TAG_NAME, "a")
                    company_name = company_link.text.strip()
                    company_url = company_link.get_attribute("href")
                    company_data.append((company_name, company_url))
                except Exception as e:
                    print(f"Error extracting company data: {e}")
                    continue

        except Exception as e:
            print(f"Error while extracting table on page: {e}")

        return company_data

    def extract_ebitda(self, company_url):
        """Extracts EBITDA data for a given company URL."""
        self.driver.get(company_url)
        print(f"Visiting: {company_url}")
        time.sleep(5)

        try:
            ebitda_label = self.driver.find_element(By.XPATH, "//td[contains(text(), 'Ebitda 2023')]")
            ebitda_value = ebitda_label.find_element(By.XPATH, "following-sibling::td").text.strip()
            ebitda_value_clean = ebitda_value.replace("€", "").replace(".", "").strip()
            return float(ebitda_value_clean.replace(",", ""))
        except Exception as e:
            print(f"Error extracting EBITDA: {e}")
            return "N/A"

    def extract_cif(self, cleaned_name):
        """Extracts CIF data for a given company name."""
        self.driver.get(f"https://www.datoscif.es/empresa/{cleaned_name}")
        print(f"Visiting: https://www.datoscif.es/empresa/{cleaned_name}")
        time.sleep(5)

        try:
            tax_id_element = self.driver.find_element(By.CSS_SELECTOR, "span[itemprop='taxID']")
            return tax_id_element.text
        except Exception as e:
            print(f"Error extracting CIF: {e}")
            return "N/A"

    def close(self):
        """Closes the Selenium driver."""
        self.driver.quit()


class DataSaver:
    """Saves extracted data to a CSV file."""

    @staticmethod
    def save_to_csv(data, filename="companies.csv"):
        """Saves the DataFrame to a CSV file."""
        data.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"Data saved to {filename}.")


class CompanyDataExtractor:
    """Orchestrates the extraction and processing of company data."""

    def __init__(self):
        self.scraper = WebScraper()
        self.cleaner = CompanyNameCleaner()
        self.saver = DataSaver()

    def run(self):
        """Main method to execute the extraction process."""
        try:
            # Step 1: Extract company names and URLs
            company_data = self.scraper.get_company_data("https://ranking-empresas.eleconomista.es/ranking_empresas_nacional.html")
            df = pd.DataFrame(company_data, columns=["Nombre de la empresa", "Fuente de la información"])

            # Step 2: Extract EBITDA and CIF
            ebitda_data = []
            cif_data = []
            cif_urls = []

            for index, row in df.iterrows():
                company_name = row["Nombre de la empresa"]
                company_url = row["Fuente de la información"]

                cleaned_name = self.cleaner.clean_company_name(company_name)

                ebitda = self.scraper.extract_ebitda(company_url)
                ebitda_data.append(ebitda)
                cif_urls.append(company_url)

                cif = self.scraper.extract_cif(cleaned_name)
                cif_data.append(cif)

            # Step 3: Add extracted data to DataFrame
            df["EBITDA 2023"] = ebitda_data
            df["CIF"] = cif_data
            df["Fuente de la información CIF"] = cif_urls
            df.rename(columns={"Fuente de la información": "Fuente de la información EBITDA"}, inplace=True)

            # Step 4: Filter and save data
            df = df[["Nombre de la empresa", "Fuente de la información EBITDA", "Fuente de la información CIF", "CIF", "EBITDA 2023"]]
            df = df[df["EBITDA 2023"].apply(lambda x: isinstance(x, (int, float)) and x > 3000000)]
            df = df[df["CIF"] != "N/A"]

            self.saver.save_to_csv(df)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.scraper.close()


if __name__ == "__main__":
    extractor = CompanyDataExtractor()
    extractor.run()