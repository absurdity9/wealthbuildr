
function submitFModelForm() {
    var form = document.getElementById('createFModelForm');
    var formData = new FormData(form);

    fetch("{% url 'create_fmodel' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            closeModal('fmodelModal');
            location.reload(); 
        }
    })
    .catch(error => console.error('Error:', error));
}

function submitIncomeForm() {
    var form = document.getElementById('createIncomeForm');
    var formData = new FormData(form);

    fetch("{% url 'create_income' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            closeModal('incomeModal');
            location.reload(); 
        }
    })
    .catch(error => console.error('Error:', error));
}

let expenseCount = 1;

function addExpenseEntry() {
    const expensesContainer = document.getElementById('expensesContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'expense-entry';
    newEntry.innerHTML = `
        <label for="expense_name_${expenseCount}">Expense Name:</label>
        <input type="text" id="expense_name_${expenseCount}" name="expense_name" required>
        <label for="expense_value_${expenseCount}">Amount:</label>
        <input type="number" step="0.01" id="expense_value_${expenseCount}" name="value" required>
    `;
    expensesContainer.appendChild(newEntry);
    expenseCount++;
}

function submitExpenseForm() {
    const form = document.getElementById('createExpenseForm');
    const formData = new FormData(form);
    const expensesContainer = document.getElementById('expensesContainer');
    const expenseEntries = expensesContainer.getElementsByClassName('expense-entry');

    const expenses = [];
    for (let i = 0; i < expenseEntries.length; i++) {
        const expenseName = expenseEntries[i].querySelector(`[id^='expense_name_']`).value;
        const expenseValue = expenseEntries[i].querySelector(`[id^='expense_value_']`).value;
        expenses.push({
            expense_name: expenseName,
            value: expenseValue
        });
    }

    const data = {
        user_id: formData.get('user_id'),
        fmodel_name: formData.get('fmodel_name'),
        expenses: expenses
    };

    const csrftoken = formData.get('csrfmiddlewaretoken');

    fetch('{% url "create_expense" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data); // Log the response to the console
        if (data.error) {
            alert(data.error);
        } else {
            alert('Expenses created successfully');
            // Optionally, update the UI with the new expense data
        }
    })
    .catch(error => console.error('Error:', error));
}

let assetCount = 1;

function addAssetEntry() {
    const assetsContainer = document.getElementById('assetsContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'asset-entry';
    newEntry.innerHTML = `
        <label for="asset_name_${assetCount}">Asset Name:</label>
        <input type="text" id="asset_name_${assetCount}" name="asset_name" required>
        <label for="yield_rate_${assetCount}">Yield Rate:</label>
        <input type="number" step="0.01" id="yield_rate_${assetCount}" name="yield_rate" required>
        <label for="principle_amount_${assetCount}">Principle Amount:</label>
        <input type="number" step="0.01" id="principle_amount_${assetCount}" name="principle_amount" required>
    `;
    assetsContainer.appendChild(newEntry);
    assetCount++;
}

function submitAssetForm() {
    const form = document.getElementById('createAssetForm');
    const formData = new FormData(form);
    const assetsContainer = document.getElementById('assetsContainer');
    const assetEntries = assetsContainer.getElementsByClassName('asset-entry');

    const assets = [];
    for (let i = 0; i < assetEntries.length; i++) {
        const assetName = assetEntries[i].querySelector(`[id^='asset_name_']`).value;
        const yieldRate = assetEntries[i].querySelector(`[id^='yield_rate_']`).value;
        const principleAmount = assetEntries[i].querySelector(`[id^='principle_amount_']`).value;
        assets.push({
            asset_name: assetName,
            yield_rate: yieldRate,
            principle_amount: principleAmount
        });
    }

    const data = {
        user_id: formData.get('user_id'),
        fmodel_name: formData.get('fmodel_name'),
        assets: assets
    };

    const csrftoken = formData.get('csrfmiddlewaretoken');

    fetch('{% url "create_assets" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data); // Log the response to the console
        if (data.error) {
            alert(data.error);
        } else {
            alert('Assets created successfully');
            // Optionally, update the UI with the new asset data
        }
    })
    .catch(error => console.error('Error:', error));
}

function submitEditFmodelForm() {
    const form = document.getElementById('editFmodelForm');
    const formData = new FormData(form);
    const new_name = formData.get('fmodel_name');
    const csrftoken = formData.get('csrfmiddlewaretoken');

    fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ new_name: new_name })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data);
        if (data.error) {
            alert(data.error);
        } else {
            alert('FModel name updated successfully');
            // Optionally, update the UI with the new FModel name
        }
    })
    .catch(error => console.error('Error:', error));
}