import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clean_company_name(company_name):
    """
    Cleans and standardizes the company name by removing special characters, replacing spaces with hyphens,
    and handling specific abbreviations like 'SAU', 'SLU', etc.

    Input:
        company_name (str): The raw company name to be cleaned.

    Output:
        str: The cleaned and standardized company name.
    """

    company_name = company_name.replace(".", "").replace(",", "").replace(" & ", "-").lower().replace(" ", "-")
    company_name = company_name.replace("ñ", "n")  # Replace 'ñ' with 'n'

    company_name = re.sub(r'[()]', '', company_name)

    company_name = re.sub(r'\-sau$', '-sa', company_name)

    company_name = re.sub(r'\-slu$', '-sl', company_name)

    company_name = re.sub(r'\-sociedad\-anonima.*$', '-sa', company_name, flags=re.IGNORECASE)

    company_name = re.sub(r'\-sociedad\-limitada.*$', '-sl', company_name, flags=re.IGNORECASE)

    return company_name


def main():
    """
    Main function to scrape company data from the ranking website, extract EBITDA and CIF information,
    and save the results to a CSV file.

    Input:
        None

    Output:
        None (saves the results to 'companies.csv')
    """
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get("https://ranking-empresas.eleconomista.es/ranking_empresas_nacional.html")

        time.sleep(5)

        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "didomi-notice-agree-button"))
            )
            submit_button.click()
            print("Agree and close clicked.")
        except Exception as e:
            print(f"Error: {e} - Agree button not found or already clicked.")

        time.sleep(5)

        company_data = []

        try:
            table = driver.find_element(By.ID, "tabla-ranking")
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

        df = pd.DataFrame(company_data, columns=["Nombre de la empresa", "Fuente de la información"])

        ebitda_data = []
        cif_data = []
        cif_urls = []

        for index, row in df.iterrows():
            company_name = row["Nombre de la empresa"]
            company_url = row["Fuente de la información"]

            cleaned_name = clean_company_name(company_name)

            driver.get(company_url)
            print(f"Visiting: {company_url}")

            time.sleep(5)

            try:
                ebitda_label = driver.find_element(
                    By.XPATH, "//td[contains(text(), 'Ebitda 2023')]"
                )
                ebitda_value = ebitda_label.find_element(
                    By.XPATH, "following-sibling::td"
                ).text.strip()

                ebitda_value_clean = ebitda_value.replace("€", "").replace(".", "").strip()

                ebitda_value_clean = float(ebitda_value_clean.replace(",", ""))

                ebitda_data.append(ebitda_value_clean)
                cif_urls.append(company_url)

            except Exception as e:
                print(f"Error extracting EBITDA for {company_name}: {e}")
                ebitda_data.append("N/A")
                cif_urls.append(company_url)

            driver.get(f"https://www.datoscif.es/empresa/{cleaned_name}")
            print(f"Visiting: https://www.datoscif.es/empresa/{cleaned_name}")
            time.sleep(5)

            try:
                tax_id_element = driver.find_element(By.CSS_SELECTOR, "span[itemprop='taxID']")
                cif_data.append(tax_id_element.text)
            except Exception as e:
                print(f"Error extracting CIF for {company_name}: {e}")
                cif_data.append("N/A")

        driver.quit()

        df["EBITDA 2023"] = ebitda_data
        df["CIF"] = cif_data

        df["Fuente de la información CIF"] = cif_urls

        df.rename(columns={"Fuente de la información": "Fuente de la información EBITDA"}, inplace=True)

        df = df[["Nombre de la empresa", "Fuente de la información EBITDA", "Fuente de la información CIF", "CIF", "EBITDA 2023"]]

        df = df[df["EBITDA 2023"].apply(lambda x: isinstance(x, (int, float)) and x > 3000000)]
        df = df[df["CIF"] != "N/A"]

        df.to_csv("companies.csv", index=False, encoding="utf-8-sig")

        print("EBITDA extraction complete. The results have been added to 'companies.csv'.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()