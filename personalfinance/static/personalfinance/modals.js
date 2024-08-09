function saveEdits() {
    // Get the fmodelId from local storage
    let fmodelId = localStorage.getItem('fmodelId');

    // Fetch the existing data for the financial model
    fetch(`/get_fmodel_data/${fmodelId}/`)
        .then(response => response.json())
        .then(data => {
            // Create an empty object to store the changed values
            let changedData = {};
            // Check if the model name has been changed
            let modelName = document.getElementById('model_name').value;
            if (modelName !== data.model_name) {
                changedData.model_name = modelName;
            }

            // Check if any income values have been changed
            let incomesContainer = document.getElementById('incomesContainer');
            let changedIncomes = [];
            for (let i = 0; i < incomesContainer.children.length; i++) {
                let incomeName = incomesContainer.children[i].querySelector(`input[name="income_name_${i}"]`).value;
                let incomeValue = incomesContainer.children[i].querySelector(`input[name="income_value_${i}"]`).value;
                if (incomeName !== data.incomes[i].income_name || incomeValue !== data.incomes[i].value) {
                    changedIncomes.push({ income_name: incomeName, value: incomeValue });
                }
            }
            if (changedIncomes.length > 0) {
                changedData.incomes = changedIncomes;
            }

            // Check if any expense values have been changed
            let expensesContainer = document.getElementById('expensesContainer');
            let changedExpenses = [];
            for (let i = 0; i < expensesContainer.children.length; i++) {
                let expenseName = expensesContainer.children[i].querySelector(`input[name="expense_name_${i}"]`).value;
                let expenseValue = expensesContainer.children[i].querySelector(`input[name="expense_value_${i}"]`).value;
                if (expenseName !== data.expenses[i].expense_name || expenseValue !== data.expenses[i].value) {
                    changedExpenses.push({ expense_name: expenseName, value: expenseValue });
                }
            }
            if (changedExpenses.length > 0) {
                changedData.expenses = changedExpenses;
            }

            // Check if any asset values have been changed
            let assetsContainer = document.getElementById('assetsContainer');
            let changedAssets = [];
            for (let i = 0; i < assetsContainer.children.length; i++) {
                let assetName = assetsContainer.children[i].querySelector(`input[name="asset_name_${i}"]`).value;
                let yieldRate = assetsContainer.children[i].querySelector(`input[name="yield_rate_${i}"]`).value;
                let principleAmount = assetsContainer.children[i].querySelector(`input[name="principle_amount_${i}"]`).value;
                if (assetName !== data.assets[i].asset_name || yieldRate !== data.assets[i].yield_rate || principleAmount !== data.assets[i].principle_amount) {
                    changedAssets.push({ asset_name: assetName, yield_rate: yieldRate, principle_amount: principleAmount });
                }
            }
            if (changedAssets.length > 0) {
                changedData.assets = changedAssets;
            }

            // Convert the changedData object to a JSON string
            let jsonBody = JSON.stringify(changedData);
            console.log(jsonBody)
            // Send the JSON string to the server using a fetch request
            fetch(`/edit_fmodel/${fmodelId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: jsonBody
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    closeModal();
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.message || 'An error occurred'));
                }
            })
            .catch(error => console.error('Error:', error));
        })
        .catch(error => console.error('Error:', error));
}

function openShareModal() {
    document.getElementById('shareModal').classList.add('is-active');
}

function closeShareModal() {
    document.getElementById('shareModal').classList.remove('is-active');
}

function showShareModal(fmodelId) {
    fetch(`/get_fmodel_data/${fmodelId}/`)
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('fmodelId', fmodelId);

            const modelName = data.model_info.model_name;
            document.getElementById('share_model_name').value = modelName;

            // Generate slug by replacing spaces with hyphens
            const slug = modelName.toLowerCase().replace(/\s+/g, '-');
            document.getElementById('slug').value = slug;

            // Open the share modal
            document.getElementById('shareModal').classList.add('is-active');
        })
        .catch(error => console.error('Error fetching model data:', error));
}

// Close modal function (reuse from edit modal)
window.closeModal = function() {
    document.getElementById('shareModal').classList.remove('is-active');
};

function publishPage() {
    const fmodelId = localStorage.getItem('fmodelId');
    const visibility = document.querySelector('input[name="visibility"]:checked').value;
    const slug = document.getElementById('slug').value;
    const pageName = document.getElementById('share_model_name').value;

    const data = {
        'is_public': visibility === 'public',
        'slug': slug,
        'page_name': pageName,
        'fmodel': fmodelId
    };

    fetch('/publish/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            alert('Page published successfully!');
            closeShareModal(); // Close the modal after publishing
        } else {
            alert('Failed to publish the page.');
        }
    })
    .catch(error => console.error('Error publishing page:', error));
}
