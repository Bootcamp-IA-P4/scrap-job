// Fetch all companies and display them
async function fetchCompanies() {
    const response = await fetch("http://127.0.0.1:8000/companies/");
    const companies = await response.json();
    const companiesList = document.getElementById("companies-list");

    companiesList.innerHTML = ""; // Clear the list
    companies.forEach(company => {
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.textContent = `${company.company_name} (CIF: ${company.cif}) - EBITDA 2023: ${company.ebitda_2023}`;

        // Add a delete button
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.classList.add("delete-button");
        deleteButton.addEventListener("click", async () => {
            await deleteCompany(company.cif);
            fetchCompanies(); // Refresh the list
        });

        li.appendChild(deleteButton);
        companiesList.appendChild(li);
    });

    // Show the companies card and "Hide Companies" button
    document.getElementById("companies-card").style.display = "block";
    document.getElementById("hide-companies-button").style.display = "inline-block";
    document.getElementById("fetch-companies-button").style.display = "none";
}

// Hide the companies list
function hideCompanies() {
    document.getElementById("companies-card").style.display = "none";
    document.getElementById("hide-companies-button").style.display = "none";
    document.getElementById("fetch-companies-button").style.display = "inline-block";
}

// Add a new company
document.getElementById("add-company-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const newCompany = {
        company_name: document.getElementById("company-name").value,
        ebitda_source: document.getElementById("ebitda-source").value,
        cif_source: document.getElementById("cif-source").value,
        cif: document.getElementById("cif").value,
        ebitda_2023: parseFloat(document.getElementById("ebitda-2023").value)
    };

    const response = await fetch("http://127.0.0.1:8000/companies/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newCompany)
    });

    if (response.ok) {
        alert("Company added successfully!");
        fetchCompanies(); // Refresh the list

        // Manually clear the form fields
        document.getElementById("company-name").value = "";
        document.getElementById("ebitda-source").value = "";
        document.getElementById("cif-source").value = "";
        document.getElementById("cif").value = "";
        document.getElementById("ebitda-2023").value = "";
        console.log("Form fields cleared manually!"); // Debugging
    } else {
        alert("Failed to add company.");
    }
});

// Search for a company by CIF
document.getElementById("search-company-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const cif = document.getElementById("search-cif").value;
    const response = await fetch(`http://127.0.0.1:8000/companies/${cif}`);
    const searchResult = document.getElementById("search-result");

    if (response.ok) {
        const company = await response.json();
        searchResult.innerHTML = `
            <strong>Company Name:</strong> ${company.company_name}<br>
            <strong>CIF:</strong> ${company.cif}<br>
            <strong>EBITDA 2023:</strong> ${company.ebitda_2023}
        `;
    } else {
        searchResult.innerHTML = "Company not found.";
    }
});

// Delete a company by CIF
async function deleteCompany(cif) {
    // Ask for confirmation
    const isConfirmed = confirm("Are you sure you want to delete this company?");
    if (!isConfirmed) return; // Stop if the user cancels

    const response = await fetch(`http://127.0.0.1:8000/companies/${cif}`, {
        method: "DELETE"
    });

    if (response.ok) {
        alert("Company deleted successfully!");
        fetchCompanies(); // Refresh the list
    } else {
        alert("Failed to delete company.");
    }
}

// Show companies when the "Show All Companies" button is clicked
document.getElementById("fetch-companies-button").addEventListener("click", fetchCompanies);

// Hide companies when the "Hide Companies" button is clicked
document.getElementById("hide-companies-button").addEventListener("click", hideCompanies);