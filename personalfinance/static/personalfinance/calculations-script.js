/*
function calculateNetSalary(annualGrossSalary) {
    // Calculate income tax
    const personalAllowance = 12570;
    const basicRateThreshold = 50270;
    const basicRate = 0.2;
    const higherRate = 0.4;
  
    let taxableIncome = annualGrossSalary - personalAllowance;
    let incomeTax = 0;
  
    if (taxableIncome > 0) {
        if (taxableIncome <= basicRateThreshold) {
            incomeTax = taxableIncome * basicRate;
        } else {
            const basicTax = basicRateThreshold * basicRate;
            const additionalTax = (taxableIncome - basicRateThreshold) * higherRate;
            incomeTax = basicTax + additionalTax;
        }
    }
  
    // Deduct employees' Class 1 National Insurance contributions (NICs)
    const nicsLowerThreshold = 6396;
    const nicsRate = 0.12;
    let nics = 0;
  
    if (annualGrossSalary > nicsLowerThreshold) {
        nics = (annualGrossSalary - nicsLowerThreshold) * nicsRate;
    }
  
    // Convert income tax and NICs to monthly figures
    const monthlyIncomeTax = incomeTax / 12;
    const monthlyNICs = nics / 12;
  
    // Calculate net annual salary
    const netAnnualSalary = annualGrossSalary - incomeTax - nics;
  
    return netAnnualSalary;
}
*/

function calculateROI(initialAmount, yieldRate, duration) {
  let accumulatedAmount = initialAmount * (1 + yieldRate / 100); 
  let yearlyAmounts = [accumulatedAmount];

  for (let year = 1; year < duration; year++) {
      accumulatedAmount = (accumulatedAmount + initialAmount) * (1 + yieldRate / 100);
      yearlyAmounts.push(accumulatedAmount);
  }

  return {
      total: accumulatedAmount,
      yearlyAmounts: yearlyAmounts
  };
}

function formatDate(datetime) {
  const date = new Date(datetime);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based, so add 1
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function calculateFutureValue(initialSavings, monthlyContribution, annualRate, months, allocPct) {
  const monthlyRate = annualRate / 12;
  
  const futureValueInitialSavings = initialSavings * Math.pow(1 + monthlyRate, months);
  
  const futureValueMonthlyContributions = (allocPct*monthlyContribution) * (Math.pow(1 + monthlyRate, months) - 1) / monthlyRate;
  
  const totalFutureValue = futureValueInitialSavings + futureValueMonthlyContributions;
  
  return totalFutureValue.toFixed(2); 
}
