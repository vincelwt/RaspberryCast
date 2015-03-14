function saveSettings() {
	localStorage.raspip = document.getElementById("raspip").value;
	localStorage.rasport = document.getElementById("rasport").value;
	var radios = document.getElementsByName('cmFunction');
	for (var i = 0, length = radios.length; i < length; i++) {
	    if (radios[i].checked) {
		localStorage.cmFunction = radios[i].value;
		break;
	    }
	}
	alert("Settings were successfully saved !");
}

document.addEventListener("DOMContentLoaded", function() {
	if (localStorage.raspip != undefined) {
		document.getElementById("raspip").value = localStorage.raspip;
		
	}

	if (localStorage.rasport == undefined) {
		localStorage.rasport = "2020";
		document.getElementById("rasport").value = localStorage.rasport;
	} else {
		document.getElementById("rasport").value = localStorage.rasport;
	}

	if (localStorage.cmFunction == undefined) {
		localStorage.rasport = "stream";
		document.getElementById("cmFstream").checked = true;
	} else {
		if (localStorage.cmFunction == "stream") {
			document.getElementById("cmFstream").checked = true;
		} else {
			document.getElementById("cmFqueue").checked = true;
		}
	}

	var el;
	el = document.getElementById("saveButton");
	el.addEventListener("click", saveSettings, false);
});
