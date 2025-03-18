import pytest
from unittest.mock import patch, MagicMock
from ..scrap import main

@patch('selenium.webdriver.Chrome')
def test_table_extraction(mock_driver):
    # Mock the table and rows
    mock_row = MagicMock()
    mock_cell = MagicMock()
    mock_link = MagicMock(text="Company 1", get_attribute=MagicMock(return_value="http://example.com"))

    mock_cell.find_element.return_value = mock_link
    mock_row.find_elements.return_value = [MagicMock(), MagicMock(), mock_cell]  # Mock 3 cells
    mock_driver.find_element.return_value.find_elements.return_value = [mock_row]

    # Call the scraping logic
    main()

    # Assert that the company name and URL were extracted correctly
    # (You can add additional assertions based on the expected behavior)

@patch('selenium.webdriver.Chrome')
def test_error_handling_missing_table(mock_driver):
    # Mock the table as missing
    mock_driver.find_element.side_effect = Exception("Table not found")

    # Call the scraping logic
    main()

    # Assert that the error was handled gracefully
    # (You can check logs or other side effects)

@patch('selenium.webdriver.Chrome')
def test_ebitda_extraction(mock_driver):
    # Mock the EBITDA label and value
    mock_ebitda_label = MagicMock()
    mock_ebitda_value = MagicMock(text="1,000,000 €")

    mock_ebitda_label.find_element.return_value = mock_ebitda_value
    mock_driver.find_element.return_value = mock_ebitda_label

    # Call the scraping logic
    main()

    # Assert that the EBITDA value was extracted and cleaned correctly
    # (You can add additional assertions based on the expected behavior)

@patch('selenium.webdriver.Chrome')
def test_cif_extraction(mock_driver):
    # Mock the CIF span
    mock_cif_span = MagicMock(text="A12345678")
    mock_driver.find_element.return_value = mock_cif_span

    # Call the scraping logic
    main()

    # Assert that the CIF value was extracted correctly
    # (You can add additional assertions based on the expected behavior)