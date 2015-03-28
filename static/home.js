$('#search').submit(function () {
	var terms = $("#search_term").val();
	showMovies("seeds", "1", "&query_term="+terms);
	return false;
});

function showMovies(sortby, page, other) {
	$('body').css("background-image", "");
	$("#overlay").hide();
	$("#infos").hide();
	$("#home").show();
	$('#results').html("");
	$('#results').append("<p id='actual_sort' hidden>"+sortby+"</p>");
	console.log("https://yts.to/api/v2/list_movies.jsonp?limit=50&sort_by="+sortby+"&page="+page+other);
	$.ajax({
	    url: "https://yts.to/api/v2/list_movies.jsonp?limit=50&sort_by="+sortby+"&page="+page+other,
	    dataType: 'jsonp',
	    success: function(results){
		$.each(results.data.movies, function(i, item) {
			var title = results.data.movies[i].title;
			var id = results.data.movies[i].id;
			var year = results.data.movies[i].year;
			var img_cover = results.data.movies[i].medium_cover_image;
			$('#results').append('<div class="element animated fadeIn"><img class="poster" onClick="showInfos('+id+');" src="'+img_cover+'" ><p class="title">'+title+'</p><p class="year">'+year+'</p></div>');
		})
	    }
	});
}

function showInfos(id) {
	$("#infos").show();
	$("#overlay").show();
	$("#home").hide();
	$('#infos').html("");
	var ip = $('#ip').text();
	$.ajax({
		url: "https://yts.to/api/v2/movie_details.jsonp?movie_id="+id+"&with_images=true",
		dataType: 'jsonp',
		success: function(results){
			var title = results.data.title;	
			var img_cover = results.data.images.large_cover_image;
			var year = results.data.year;
			var rating = results.data.rating;
			var genres = results.data.genres;
			var runtime = results.data.runtime;
			var description = results.data.description_full;
			var background_image = results.data.images.background_image;	
			var yt_trailer = results.data.yt_trailer_code;
			
			$('#infos').append('<img class="detail_poster" src="'+img_cover+'" >');
			$('#infos').append('<h1 class="detail_title">'+title+'</p>');
			$('#infos').append('<p class="detail_infos">'+year+' - '+runtime+' min - '+rating+'/10 - '+genres+'</p>');
			$('#infos').append('<p class="detail_description">'+description+'</p>');
			$('#infos').append('<a id="close-btn" onClick="closeInfos()"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></a>');
			$('body').css('background-image', 'url(' + background_image + ')');
			$.each(results.data.torrents, function(i, item) {
				var url = results.data.torrents[i].url;
				var quality = results.data.torrents[i].quality;
				if (quality != "3D") {
					$('#infos').append('<a class="btn btn-lg btn-danger" href="http://'+ip+':2020/torrent?url='+url+'">'+quality+'</a>');
				}
			})
			if (yt_trailer != "") {
				$('#infos').append('<a class="btn btn-lg btn-info" href="http://'+ip+':2020/stream?url=http://youtube.com/watch?v='+yt_trailer+'">Trailer</a>');
			}
		}
	});
}

function openPage(page) {
	var actual_sort = $('#actual_sort').text();
	alert
	showMovies(actual_sort, page, '');
}

function closeInfos() {
	$('body').css("background-image", "");
	$("#overlay").hide();
	$("#infos").hide();
	$("#home").show();
}
