/* To manage history content we use localStorage to save data. */

var historyArray = [];

function storageAvailable(type) {
	try {
		var storage = window[type],
		x = '__storage_test__';
		storage.setItem(x, x);
		storage.removeItem(x);
		return true;
	}
	catch(e) {
		return e instanceof DOMException && (
            // everything except Firefox
            e.code === 22 ||
            // Firefox
            e.code === 1014 ||
            // test name field too, because code might not be present
            // everything except Firefox
            e.name === 'QuotaExceededError' ||
            // Firefox
            e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
            // acknowledge QuotaExceededError only if there's something already stored
            storage.length !== 0;
      }
}


function addToHistory(url) {
      if (storageAvailable('localStorage')) {
            //Retreive the history, create an empty array if it does not exist
            historyArray = JSON.parse(localStorage.getItem('history'));
      
            if (!historyArray)
            historyArray = [];

            url = url.replace(/\"/g, "");

            //Don't add duplicates to the history
            //A possible enhancement would be to push it to the top of the array
            if (!historyArray.includes(url))  
                  historyArray.push(url);

            localStorage.setItem('history', JSON.stringify(historyArray));
      }
}

function updateHistoryDiv() {
      if (storageAvailable('localStorage')) {
            historyArray = JSON.parse(localStorage.getItem('history'));
            
            if (!historyArray) {
                  return;
            }

            uniqueArray = historyArray.filter(function(item, pos) {
                  return historyArray.indexOf(item) == pos;
            });

            $("#history-div").empty();

            for (var i = uniqueArray.length - 1; i >= 0; i--) {

                  var historyLink = $("<a class='history-link-item' href='#'>" + uniqueArray[i] + "</a>").click(function() {
                        var encoded_url = encodeURIComponent($(this).text());
                        mkrequest("/stream?url=" + encoded_url, 1);
                  });

                  $("#history-div").append(historyLink);  //Add the link.
                  $("#history-div").append("<hr>");
            }

            var clearHistoryLink = $("<a id='clear-history-link-item' href=''>Clear history</a>").click(function() {
                  localStorage.clear();
                  $( "#history-div" ).toggle("fast");
            });

            $("#history-div").append(clearHistoryLink);  //Add the link.
            $("#history-div").append("<hr>");

      }
}