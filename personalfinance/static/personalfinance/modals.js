function saveEdits() {
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
                let allocationPct = assetsContainer.children[i].querySelector(`input[name="allocation_pct_${i}"]`).value;

                // Check if any asset field has been changed
                if (assetName !== data.assets[i].asset_name || 
                    yieldRate !== data.assets[i].yield_rate || 
                    principleAmount !== data.assets[i].principle_amount || 
                    allocationPct !== data.assets[i].allocation_pct) {
                    
                    changedAssets.push({ 
                        asset_name: assetName, 
                        yield_rate: yieldRate, 
                        principle_amount: principleAmount, 
                        allocation_pct: allocationPct 
                    });
                }
            }
            if (changedAssets.length > 0) {
                changedData.assets = changedAssets;
            }

            // Convert the changedData object to a JSON string
            let jsonBody = JSON.stringify(changedData);
            console.log(jsonBody);
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

function showShareModal(fmodelId) {
    fetch(`/get_fmodel_data/${fmodelId}/`)
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('fmodelId', fmodelId);

            const modelName = data.model_info.model_name;
            document.getElementById('share_model_name').value = modelName;

            const slug = modelName.toLowerCase().replace(/\s+/g, '-');
            document.getElementById('slug').value = slug;

            document.getElementById('shareModal').classList.add('is-active');
        })
        .catch(error => console.error('Error fetching model data:', error));
}

function closeShareModal() {
    document.getElementById('shareModal').classList.remove('is-active');
}

function showAddExpenseModal(fmodelId) {
    document.getElementById('addExpenseModal').classList.add('is-active');
}

function returnfmodelNameValue(){
    let fmodelId = localStorage.getItem('fmodelId');
    let fmodelNameValue

    fetch(`/get_fmodel_data/${fmodelId}/`)
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('fmodelId', fmodelId);
        const modelName = data.model_info.model_name;
        return modelName;
    })
    .catch(error => console.error('Error fetching model data:', error));
    modelName = fmodelNameValue;
    return fmodelNameValue
}


function closeAddExpenseModal() {
    document.getElementById('addExpenseModal').classList.remove('is-active');
}

function showAddAssetsModal() {
    document.getElementById('addAssetsModal').classList.add('is-active');
}

function closeAddAssetsModal() {
    document.getElementById('addAssetsModal').classList.remove('is-active');
}


function togglePublicStatus(data) {

    console.log("toggle status fx on");

    const requestData = {
        slug: data.slug,
        is_public: data.is_public
    };
    console.log(requestData);

    let jsonBody = JSON.stringify(requestData);

    return fetch('/toggle_public/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonBody
    })
    .then(response => response.json().then(body => {
        if (response.ok) {
            alert('Page public status toggled successfully!');
            closeShareModal(); // Close the modal after updating
        } else if (response.status === 400 && body.error) {
            alert(`Failed to toggle public status: ${body.error}`);
        } else {
            alert('Failed to toggle public status due to an unknown error.');
        }
    }))
    .catch(error => {
        console.error('Error toggling public status:', error);
        alert('Error toggling public status: ' + error.message);
    });
}

function checkPageExists(fmodelId) {
    return fetch(`/check-published-page/${fmodelId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to check page existence');
            }
            return response.json();
        })
        .then(data => data.exists)
        .catch(error => {
            console.error('Error checking page existence:', error);
            alert('Error checking page existence: ' + error.message);
            return false; // Assuming the page does not exist in case of an error
        });
}

function publishPage() {
    const fmodelId = localStorage.getItem('fmodelId');
    const visibility = document.querySelector('input[name="visibility"]:checked').value;
    const slug = document.getElementById('slug').value;
    const pageName = document.getElementById('share_model_name').value;

    const data = {
        'is_public': visibility === "True",
        'slug': slug,
        'page_name': pageName,
        'fmodel': fmodelId
    };

    checkPageExists(fmodelId).then(exists => {

        if (exists) {
            // If the page exists, toggle its public status
            togglePublicStatus({
                'slug': slug,
                'is_public': visibility === "True"
            });
        } else {
            // If the page does not exist, publish it
            fetch('/publish/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json().then(body => {
                if (response.ok) {
                    alert('Page published successfully!');
                    closeShareModal(); // Close the modal after publishing
                } else if (response.status === 400 && body.error) {
                    alert(`Failed to publish the page: ${body.error}`);
                } else {
                    alert('Failed to publish the page due to an unknown error.');
                }
            }))
            .catch(error => {
                console.error('Error publishing page:', error);
                alert('Error publishing page: ' + error.message);
            });
        }
    });
}