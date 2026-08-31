let expenses = []

// ADD EXPENSE
// ADD EXPENSE FUNCTION
async function addExpense(){

let category=document.getElementById("category").value
let amount=parseFloat(document.getElementById("amount").value)

await fetch("/add_expense",{

method:"POST",

headers:{"Content-Type":"application/json"},

body:JSON.stringify({
user:"demo",
category:category,
amount:amount
})

})

alert("Expense Added")

checkAnomaly()

}

// send to backend
await fetch("/add_expense",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
user:"demo",
category:category,
amount:amount
})

})

// store locally
expenses.push({
category:category,
amount:amount
})

alert("Expense Added")

// update chart
loadChart()

// check anomaly
checkAnomaly()

}


// CALCULATE SUMMARY + ML CLASSIFICATION + PREDICTION
async function calculateSummary(){

let salary = parseFloat(document.getElementById("salary").value)

let total = expenses.reduce((sum,e)=>sum+e.amount,0)

let savings = salary - total

document.getElementById("totalExpense").innerHTML =
"Total Expense: ₹" + total

document.getElementById("savings").innerHTML =
"Remaining Savings: ₹" + savings


// CALL ML CLASSIFICATION
let res = await fetch("/classify",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
income:salary,
expense:total
})

})

let data = await res.json()

document.getElementById("classification").innerHTML =
"Spending Type: " + data.classification


// GET EXPENSE PREDICTION
let p = await fetch("/predict")

let pdata = await p.json()

document.getElementById("prediction").innerHTML =
"Predicted Next Expense: ₹" + pdata.prediction

}


// LOAD PIE CHART
function loadChart(){

let labels = expenses.map(x=>x.category)
let values = expenses.map(x=>x.amount)

let ctx = document.getElementById("expenseChart")

// destroy old chart
if(window.expenseChart){
window.expenseChart.destroy()
}

window.expenseChart = new Chart(ctx,{

type:"pie",

data:{
labels:labels,
datasets:[{
label:"Expenses",
data:values
}]
},

options:{
responsive:true,
animation:{
animateRotate:true,
animateScale:true
}
}

})

}


// CHECK ANOMALY
async function checkAnomaly(){

let res = await fetch("/anomaly")

let data = await res.json()

if(data.anomaly.includes(-1)){

document.getElementById("anomaly").innerHTML =
"⚠ Unusual expense detected!"

}

}