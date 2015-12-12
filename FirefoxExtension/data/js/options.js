function saveSettings() {
	localStorage.raspip = document.getElementById("raspip").value;

	var radios = document.getElementsByName('cmFunction');
	for (var i = 0, length = radios.length; i < length; i++) {
	    if (radios[i].checked) {
		localStorage.cmFunction = radios[i].value;
		break;
	    }
	}

	var radios = document.getElementsByName('mode_slow');
	for (var i = 0, length = radios.length; i < length; i++) {
	    if (radios[i].checked) {
		localStorage.modeslow = radios[i].value;
		break;
	    }
	}

	alert("Settings were successfully saved !");
}

document.addEventListener("DOMContentLoaded", function() {
	if (localStorage.raspip != undefined) {
		document.getElementById("raspip").value = localStorage.raspip;
	} else {
		document.getElementById("raspip").value = "raspberrypi.local";
		localStorage.raspip = 'raspberrypi.local';
	}
localStorage.raspip
	if (localStorage.cmFunction == undefined) {
		localStorage.cmFunction = "stream";
		document.getElementById("cmFstream").checked = true;
	} else {
		if (localStorage.cmFunction == "stream") {
			document.getElementById("cmFstream").checked = true;
		} else {
			document.getElementById("cmFqueue").checked = true;
		}
	}

	if (localStorage.modeslow == undefined) {
		localStorage.modeslow = "False";
		document.getElementById("high_qual").checked = true;
	} else {
		if (localStorage.modeslow == "False") {
			document.getElementById("high_qual").checked = true;
		} else {
			document.getElementById("bad_qual").checked = true;
		}
	}

	var el = document.getElementById("saveButton");
	el.addEventListener("click", saveSettings, false);
});
