/* Handle all logic related to managing the queue in the remote view */

function updateQueueDiv() {
	//TODO: Handle removing and re-ordering of items within the queue
}

function addToQueueUI(url) {
	var queueDiv = $("#queue-div");
	var listItemDiv = $("<div>");
	listItemDiv.addClass("list-item")

	if (url.includes("youtu")) {
		var id = extractIDFromURL(url)
		var title = extractTitleFromURL(url)
		var imgSrc = "http://img.youtube.com/vi/" + id + "/0.jpg"

		listItemDiv.append('<img class="item-image" src="' + imgSrc + '" />')
		listItemDiv.append('<span class="item-text">' + title + '</span>')
		
	}
	else if (url.includes("soundcloud")) {
		listItemDiv.append('<img class="item-image" src="/static/music.svg"/>')
		listItemDiv.append('<span class="item-text">' + url + '</span>')
		
	}
	else {
		listItemDiv.append('<img class="item-image" src="/static/film.svg"/>')
		listItemDiv.append('<span class="item-text">' + url + '</span>')
	}

	queueDiv.append(listItemDiv);
	queueDiv.append("<hr>");
}

function extractIDFromURL(url) {
	var regExp = /.*(?:youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*/;
    var match = url.match(regExp);
    return (match&&match[1].length==11)? match[1] : false;
}

function extractTitleFromURL(url) {
	//https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=KesLVRj4yIU&format=json
	return url;
}