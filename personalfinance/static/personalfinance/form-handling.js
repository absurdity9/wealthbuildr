let expenseCount = 1;

function addExpenseEntry() {
  const expensesContainer = document.getElementById("expensesContainer");
  const newEntry = document.createElement("div");
  newEntry.className = "expense-entry block"; // Added Bulma block styling for separation
  newEntry.innerHTML = `
        <div class="field">
            <label for="expense_name_${expenseCount}" class="label">Expense Name:</label>
            <div class="control">
                <input type="text" id="expense_name_${expenseCount}" name="expense_name" class="input" required>
            </div>
        </div>
        <div class="field">
            <label for="expense_value_${expenseCount}" class="label">Amount (£):</label>
            <div class="control">
                <input type="number" step="0.01" id="expense_value_${expenseCount}" name="value" class="input" required>
            </div>
        </div>
    `;
  expensesContainer.appendChild(newEntry);
  expenseCount++;
}

let assetCount = 1;

function addAssetEntry() {
  const assetsContainer = document.getElementById("assetsContainer");
  const newEntry = document.createElement("div");
  newEntry.className = "asset-entry block"; // Added Bulma block styling for separation
  newEntry.innerHTML = `
        <div class="field">
            <label for="asset_name_${assetCount}" class="label">Asset Name:</label>
            <div class="control">
                <input type="text" id="asset_name_${assetCount}" name="asset_name" class="input" required>
            </div>
        </div>
        <div class="field">
            <label for="yield_rate_${assetCount}" class="label">Yield Rate:</label>
            <div class="control">
                <input type="number" step="0.01" id="yield_rate_${assetCount}" name="yield_rate" class="input" required>
            </div>
        </div>
        <div class="field">
            <label for="principle_amount_${assetCount}" class="label">Principal Amount (£):</label>
            <div class="control">
                <input type="number" step="0.01" id="principle_amount_${assetCount}" name="principle_amount" class="input" required>
            </div>
        </div>
        <div class="field">
            <label for="yield_rate_0" class="label">Allocation of leftover cash (%):</label>
            <div class="control">
                <input type="number" step="0.01" id="allocation_pct" name="allocation_pct" class="input" required>
            </div>
        </div>
    `;
  assetsContainer.appendChild(newEntry);
  assetCount++;
}

