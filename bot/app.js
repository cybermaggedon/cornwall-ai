
function submit() {

    var q_elt = document.getElementById("question");

    let question = q_elt.value;

    q_elt.value = "";

    ask_question(question);

    return false;
    
}

function show_text(answer, div) {

    let a_div = document.createElement("div");
    a_div.className = "answertext";
    a_div.appendChild(document.createTextNode(answer["answer"]));

    div.appendChild(a_div);

}

function show_table(answer, div) {

    let table = answer["table"];
    let columns = answer["columns"];

    let numrows = table[columns[0]].length;

    if (numrows == 0) {
	div.appendChild(document.createTextNode("No data found"));
	return;
    }

    let tblelt = document.createElement("table");

    let thead = tblelt.createTHead();

    let row = thead.insertRow(0);

    for (let i = 0; i < columns.length; i++) {
        cell = row.insertCell(i);
	cell.appendChild(document.createTextNode(columns[i]));
    }

    for (let j = 0; j < numrows; j++) {

	let row = tblelt.insertRow(j + 1);

	for (let i = 0; i < columns.length; i++) {

	    let datum = table[columns[i]][j];

	    cell = row.insertCell(i);
	    cell.appendChild(document.createTextNode(datum));

	}

    }

    div.appendChild(tblelt);

}

function show_answer(answer, div) {

    while (div.firstChild) div.removeChild(div.firstChild);

    for (let ans of answer) {

	if (ans["class"] == "text") {
	    show_text(ans, div);
	}

	if (ans["class"] == "table") {
	    show_table(ans, div);
	}

    }
/*
    let a_div = document.createElement("div");
    a_div.className = "answertext";
    a_div.appendChild(document.createTextNode(answer));

    div.appendChild(a_div);

    let numrows = table[columns[0]].length;

    if (numrows == 0) {
	a_div.appendChild(document.createTextNode("No data found"));
	return;
    }

    let tblelt = document.createElement("table");

    let thead = tblelt.createTHead();

    let row = thead.insertRow(0);

    for (let i = 0; i < columns.length; i++) {
        cell = row.insertCell(i);
	cell.appendChild(document.createTextNode(columns[i]));
    }

    for (let j = 0; j < numrows; j++) {

	let row = tblelt.insertRow(j + 1);

	for (let i = 0; i < columns.length; i++) {

	    let datum = table[columns[i]][j];

	    cell = row.insertCell(i);
	    cell.appendChild(document.createTextNode(datum));

	}

    }

    div.appendChild(tblelt);
  */  
}

function wait_for(id, div) {

    new Promise(
	(resolve, reject) => {
	    setTimeout(resolve, 1000);
	}
    ).then(
	() => fetch("/api/question/" + id)
    ).then(
	(resp) => resp.json()
    ).then(
	(obj) => {
	    if (obj["state"] == "complete")
		show_answer(obj["answer"], div);
	    else
		wait_for(id, div);
	}
    );

}

function handle_question(q, div) {

    fetch(
	"/api/question",
	{
	    method: "PUT",
	    headers: {
		"Content-Type": "application/json",
	    },
	    body: JSON.stringify({
		question: q,
	    })
	}
    ).then(
	(resp) => resp.json()
    ).then(
	(obj) => {
	    wait_for(obj["id"], div);
	}
    );

}

function ask_question(q) {

    let elt = document.getElementById("output");

    let q_div = document.createElement("div");
    q_div.className = "dialog question";
    q_div.appendChild(document.createTextNode(q));
    elt.appendChild(q_div);

    let a_div = document.createElement("div");
    a_div.className = "dialog answer";
    elt.appendChild(a_div);


    let t_div = document.createElement("div");
    t_div.className = "lds-thinking";

    t_div.appendChild(document.createElement("div"));
    t_div.appendChild(document.createElement("div"));
    t_div.appendChild(document.createElement("div"));
    
    a_div.appendChild(t_div);

    handle_question(q, a_div);

}

function init() {

    console.log("Running.")

    document.getElementById("questionform").onsubmit = submit;

}

