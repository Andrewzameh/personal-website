var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab
const scoreDict = {
  region: { 1: 2, 2: 0, 3: 0 },
  power: { 1: -2, 2: 1, 3: 2 },
  asset: { 1: 0, 2: 0, 3: 0 }, //if 1 and region 2 = -2
  concent: { 1: -1, 2: 1 },
  EBITDA: { 1: 0, 2: 0, 3: 1, 4: 2 }, //if 1 and region 2 = -2, if 2 and region 2 = -1
  ARR: { 1: -2, 2: -1, 3: 1, 4: 2 },
  PS: { 1: 1, 2: -1, 3: -2 }, //if 2 and region 2 = -2
  gross: { 1: 2, 2: -1 },
  churn: { 1: 2, 2: 0, 3: -2 },
};
var currentScore = {
  region: 0,
  power: 0,
  asset: 0,
  concent: 0,
  EBITDA: 0,
  ARR: 0,
  PS: 0,
  gross: 0,
  churn: 0,
};
var currentValues = {
  region: 0,
  power: 0,
  asset: 0,
  concent: 0,
  EBITDA: 0,
  ARR: 0,
  PS: 0,
  gross: 0,
  churn: 0,
};

function showTab(n) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "inline";
  y = x[n].getElementsByTagName("select");
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
    document.getElementById("missioninfo").classList.remove("invisible");
    document.getElementById("message2").classList.remove("d-none");
  } else {
    document.getElementById("prevBtn").style.display = "inline";
    document.getElementById("missioninfo").className += " invisible";
  }
  if (n == x.length - 1) {
    document.getElementById("nextBtn").innerHTML = "Calculate";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  if (n != 3) {
    document.getElementById("chart-body").classList.remove("d-flex");
    document.getElementById("chart-body").classList.add("d-none");
    document.getElementById("message").className = "";
  }

  fixStepIndicator(n);
}

function nextPrev(n) {
  var x = document.getElementsByClassName("tab");
  if (currentTab == 3) {
    if (n == 1 && !validateForm(currentTab)) return false;

    if (n == 1) {
      generatePie((totalScore * 100) / 14);
      populateLists();
      console.log("currentTab: " + currentTab);
    } else {
      x[currentTab].style.display = "none";
      document.getElementById("message").innerHTML = "";
      if (currentTab + n < 0) {
        currentTab = 0;
      } else {
        currentTab = currentTab + n;
      }
      showTab(currentTab);
      console.log("currentTab: " + currentTab);
    }
  } else {
    if (n == 1 && !validateForm(currentTab)) return false;
    x[currentTab].style.display = "none";
    if (currentTab + n < 0) {
      currentTab = 0;
    } else {
      currentTab = currentTab + n;
    }

    console.log("currentTab: " + currentTab);
    showTab(currentTab);
  }
}

function validateForm(n) {
  var x,
    y,
    z,
    i,
    count = 0,
    valid = true;
  x = document.getElementsByClassName("tab");

  z = x[n].getElementsByClassName("group");
  for (var p = 0; p < z.length; p++) {
    y = z[p].getElementsByTagName("input");

    for (i = 0; i < y.length; i++) {
      if (y[i].checked) {
        count += 1;
        break;
      }
    }
  }

  if (count != z.length) {
    document.getElementById("message").innerHTML =
      "Please Answer all questions";
    document.getElementById("message").className += " alert alert-danger";

    valid = false;
  } else {
    document.getElementById("message").innerHTML = "";
    document.getElementById("message").className -= " alert alert-danger";
  }
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid;
}

function fixStepIndicator(n) {
  var i,
    x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }

  x[n].className += " active";
}

var totalScore = 0;
var questionsDivs = document.getElementsByName("question");
for (var i = 0; i < questionsDivs.length; i++) {
  var question = questionsDivs[i].getElementsByTagName("input");
  if (i == 0) {
    for (var y = 0, max = question.length; y < max; y++) {
      question[y].onclick = function () {
        if (this.value == "2") {
          document.getElementById("nextBtn").style.display = "none";
          document.getElementById("score").style.display = "none";
          document.getElementById("message").innerHTML =
            "Do Not Buy This Company";
          document.getElementById("message").className += " alert alert-danger";
        } else {
          document.getElementById("nextBtn").style.display = "inline";
          document.getElementById("score").style.display = "inline";
          document.getElementById("message").innerHTML = "";
          document.getElementById("message").className -= " alert alert-danger";
        }
      };
    }
  } else {
    for (var x = 0; x < question.length; x++) {
      question[x].onclick = function () {
        updateScore(this.name, this.value);
      };
    }
  }
}

function updateScore(name, value) {
  currentValues[name] = value;
  currentScore[name] = scoreDict[name][Number(value)];
  if (currentValues["region"] == "2") {
    if (currentValues["asset"] == "1") {
      currentScore["asset"] = -2;
    }
    if (currentValues["EBITDA"] == "1") {
      currentScore["EBITDA"] = -2;
    } else if (currentValues["EBITDA"] == "2") {
      currentScore["EBITDA"] = -1;
      // cons.push('Current EBITDA% is between -10% and 0%');
    }
    if (currentValues["PS"] == "2") {
      currentScore["PS"] = -2;
    }
  }
  var scoreLoop = 0;
  for (const key in currentScore) {
    scoreLoop += currentScore[key];
  }
  totalScore = scoreLoop;
  document.getElementById("totalScore").innerHTML = totalScore;
}

function reset() {
  var ele = document.getElementsByTagName("input");
  for (var i = 0; i < ele.length; i++) ele[i].checked = false;
}
function resetScore() {
  for (const keyx in currentScore) {
    currentScore[keyx] = 0;
    currentValues[keyx] = 0;
  }
  totalScore = 0;
  document.getElementById("totalScore").innerHTML = 0;
  document.getElementById("message").innerHTML = "";
  document.getElementById("message").className = "";
  document.getElementById("nextBtn").style.display = "inline";
  document.getElementById("score").style.display = "inline";
  document.getElementById("chart-body").classList.add("d-none");
  document.getElementById("chart-body").classList.remove("d-flex");

  myChart.destroy();
}

function generatePie(score) {
  if (score < 0) {
    score = 0;
  }
  const ctx = document.getElementById("myChart");
  var data = {
    labels: ["Yes", "No"],
    datasets: [
      {
        label: "Company Score",
        data: [score, 100 - score],
        backgroundColor: ["rgb(54, 162, 235)", "rgb(255, 99, 132)"],
        hoverOffset: 4,
      },
    ],
  };
  var config = {
    type: "pie",
    data: data,
  };

  document.getElementById("message").innerHTML =
    "Percentage: " + score.toFixed(2) + "%";
  document.getElementById("chart-body").classList.remove("d-none");
  document.getElementById("message2").classList.add("d-none");
  document.getElementById("chart-body").classList.add("d-flex");
  try {
    myChart.destroy();
  } catch (err) {
    console.log("err: " + err);
    console.log("Didn't get created yet");
  } finally {
    myChart = new Chart(ctx, config);
  }
}

function populateLists() {
  var pros = [];
  var cons = [];

  const myNodeCon = document.getElementById("cons");
  const myNodePro = document.getElementById("pros");
  myNodeCon.textContent = "";
  myNodePro.textContent = "";

  if (currentValues["region"] == "1") {
    pros.push("Region is North America");
  } else if (currentValues["region"] == "2") {
    cons.push("Region is Europe");
    if (currentValues["asset"] == "1") {
      cons.push("Asset type is Legacy");
    }
    if (currentValues["EBITDA"] == "1") {
      cons.push("Current EBITDA% is < -10%");
    }
    if (currentValues["PS"] == "2") {
      currentScore["PS"] = -2;
    }
  }
  if (currentValues["power"] == "1") {
    cons.push("Pricing Power is low");
  } else if (currentValues["power"] == "3") {
    pros.push("Pricing Power is High");
  }
  if (currentValues["concent"] == "1") {
    cons.push("Customer Concentration");
  } else if (currentValues["concent"] == "2") {
    pros.push("Customer Concentration");
  }
  if (currentValues["EBITDA"] == "4") {
    pros.push("Current EBITDA% is 10%+");
  }
  if (currentValues["ARR"] == "1") {
    cons.push("ARR% of TR is < 50%");
  } else if (currentValues["ARR"] == "4") {
    pros.push("ARR% of TR is 80%+");
  }
  if (currentValues["PS"] == "1") {
    pros.push("PS% of TR is < 25%");
  } else if (currentValues["PS"] == "2" && currentValues["region"] == "2") {
    cons.push("PS% of TR is between 25% and 40%");
  } else if (currentValues["PS"] == "3") {
    cons.push("PS% of TR is 40%+");
  }
  if (currentValues["gross"] == "1") {
    pros.push("Gross Margins is 80%+");
  } else if (currentValues["gross"] == "2") {
    cons.push("Gross Margins is < 70%");
  }
  if (currentValues["churn"] == "1") {
    pros.push("Churn is between 0% and 5%");
  } else if (currentValues["churn"] == "3") {
    cons.push("Churn is 10%+");
  }

  console.log("pros: " + pros);
  console.log("cons: " + cons);
  console.log("cons.length: " + cons.length);
  console.log("pros.length: " + pros.length);

  var consList = document.getElementById("cons");
  for (i = 0; i < cons.length; i++) {
    var li = document.createElement("li"); // create li element.
    li.setAttribute("class", "list-group-item");
    li.innerHTML = cons[i]; // assigning text to li using array value.
    consList.appendChild(li);
  }
  var prosList = document.getElementById("pros");
  for (y = 0; y < pros.length; y++) {
    var litem = document.createElement("li"); // create li element.
    litem.setAttribute("class", "list-group-item");
    litem.innerHTML = pros[y]; // assigning text to li using array value.
    prosList.appendChild(litem);
  }
}
