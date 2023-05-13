function submitForm() {
  var revisedList = getList("revised-list");
  var solvedList = getList("solved-list");
  document.getElementById("revised").value = JSON.stringify(revisedList);
  document.getElementById("solved").value = JSON.stringify(solvedList);
  document.forms[0].submit();
}

function addToList(listId, inputId) {
  var input = document.getElementById(inputId).value;
  if (input !== "") {
    if (inputId === "solved" && !/^\d+\.\s*[A-Za-z]/.test(input)) {
      var flashMsg = `Your input ${input} doesn't match this format (23. Two Sum)`;
      var flashDiv = document.createElement("div");
      flashDiv.className = "alert alert-danger";
      flashDiv.style.textAlign = "center";
      var flashText = document.createTextNode(flashMsg);
      flashDiv.appendChild(flashText);
      document.getElementById("flash-messages").appendChild(flashDiv);
      document.getElementById(inputId).value = "";
      setTimeout(function () {
        flashDiv.remove();
      }, 3000);
      return;
    }
    var li = document.createElement("li");
    var checkMark = document.createTextNode("\uD83D\uDCCC ");
    li.appendChild(checkMark);
    li.className = "list-group-item my-2";
    var text = document.createTextNode(input);
    li.appendChild(text);
    document.getElementById(listId).appendChild(li);
    document.getElementById(inputId).value = "";
  }
}

function getList(listId) {
  var listItems = document.getElementById(listId).getElementsByTagName("li");
  var items = [];
  for (var i = 0; i < listItems.length; i++) {
    items.push(listItems[i].textContent);
  }
  return items;
}

function increase() {
    // Change the variable to modify the speed of the number increasing from 0 to (ms)
    let SPEED = 55;
    // Retrieve the percentage value
    let limit = parseInt(document.getElementById("value1").innerHTML, 10);

    for(let i = 0; i <= limit; i++) {
        setTimeout(function () {
            document.getElementById("value1").innerHTML = i + "%";
        }, SPEED * i);
    }
}

increase();