var self = require('sdk/self');
var prefs = require("sdk/simple-prefs").prefs;
var buttons = require('sdk/ui/button/action');
var { ToggleButton } = require('sdk/ui/button/toggle');
var tabs = require("sdk/tabs");
var Request = require("sdk/request").Request;
var notifications = require("sdk/notifications");
var cm = require("sdk/context-menu");

var button = ToggleButton({
  id: "raspberrycast-btn",
  label: "RaspberryCast",
  icon: {
    "16": "./16.png",
    "48": "./48.png",
    "128": "./128.png"
  },
  onChange: handleChange
});

const { Panel } = require('sdk/panel');
let panel = Panel({
  contentURL: self.data.url("popup.html"),
  contentScriptFile: [self.data.url("js/jquery-2.1.3.min.js"), self.data.url("js/popup.js")],
  width: 130,
  height: 100,
  onHide: handleHide
});

function handleChange(state) {
  if (state.checked) {
  	panel.resize(130, 100);
    panel.show({
      position: button
    });

    panel.port.emit("state", "loading");

	Request({
	  url: "http://"+prefs.raspIp+":2020/running",
	  onComplete: function (response) {
	  	if (response.text == "1") {
	  		panel.port.emit("state", "playing");
	  		panel.resize(130, 215);
	  	} else {
	  		panel.port.emit("state", "idle");
	  		panel.resize(130, 100);
	  	}
	  }
	}).get();
  }
}

function handleHide() {
  button.state('window', {checked: false});
}

panel.port.on("mkrequest", function(url) {
	if (url == "/stream" || url == "/queue") {
		panel.hide();
		mkrequest(url + "?url=" + encodeURIComponent(tabs.activeTab.url) + "&slow=" + prefs.slowMode);
	} else {
		mkrequest(url);
	}
});

var script = 'self.on("click", function (node, data) {' +
                'self.postMessage(node.href);'+
              '});';

cm.Item({
  label: "Cast now",
  context: cm.SelectorContext("a[href]"),
  image: self.data.url("./16.png"),
  contentScript: script,
  onMessage: function (data) {
	mkrequest("/stream?url=" + encodeURIComponent(data) + "&slow=" + prefs.slowMode);
  }
});

cm.Item({
  label: "Add to queue",
  context: cm.SelectorContext("a[href]"),
  image: self.data.url("./16.png"),
  contentScript: script,
  onMessage: function (data) {
	mkrequest("/queue?url=" + encodeURIComponent(data) + "&slow=" + prefs.slowMode);
  }
});

function mkrequest(url) {
	if (url.indexOf("/stream") > -1 || url.indexOf("/queue") > -1) {
		notifications.notify({ title: "RaspberryCast", text: "Processing video. Please wait ~10 seconds." });
	}

	Request({
	  url: "http://"+prefs.raspIp+":2020" + url,
	  onComplete: function (response) {
	  	if (url.indexOf("/stream") > -1 || url.indexOf("/queue") > -1) {
			if (response.text == "1") {
				notifications.notify({ title: "RaspberryCast", text: "Video should start playing." });
			} else if (response.text == "2") {
				notifications.notify({ title: "RaspberryCast", text: "Video has been added to queue." });
			} else {
				notifications.notify({ title: "RaspberryCast", text: "An error occured during the request." });
			}
		}
	  }
	}).get();
}