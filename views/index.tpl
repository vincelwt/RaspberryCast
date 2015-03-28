<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8">
		<meta charset="utf-8">
		<title>RaspberryCast</title>
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
		<link href="{{get_url('static', filename='style.css') }}" rel="stylesheet">
		<link href="{{get_url('static', filename='bootstrap.min.css') }}" rel="stylesheet">
		<link href="{{get_url('static', filename='animate.css') }}" rel="stylesheet">
		<link href="{{get_url('static', filename='simple-sidebar.css') }}" rel="stylesheet">
		<link rel="icon" type="image/png" sizes="192x192" href="{{get_url('static', filename='favicon.png') }}" />
	</head>
	<body onLoad="showMovies('seeds', '1', '');">
		<p id="ip" hidden>{{ip}}</p>
		<!-- <nav class="navbar navbar-default navbar-fixed-top">
			<div class="container-fluid">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
					<span class="sr-only">Toggle navigation</span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					</button>

					<a class="navbar-brand" href="/" title="RaspberryCast"><img src="{{get_url('static', filename='favicon.png') }}" width="20px"/> </a>
				</div>
				<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
					<ul class="nav navbar-nav">
					<li><a onClick="showMovies('seeds', '1', '');">Popularity</a></li>
					<li><a onClick="showMovies('rating', '1', '');">Best rated</a></li>
					</ul>
					
				</div>
			</div>
		</nav> -->

 <div id="wrapper">
        <div id="sidebar-wrapper">
            <ul class="sidebar-nav">
                <li class="sidebar-brand">
                    <a href="/">
                        <img src="{{get_url('static', filename='favicon.png') }}" width="20px" style="margin-right: 20px;"/>RaspberryCast
                    </a>
                </li>
		<li>
			<form id="search" class="navbar-form" role="search">
				<div class="form-group">
				  <input type="text" id="search_term" class="form-control" placeholder="Search ...">
				</div>
			</form>
		</li>
                <li>
                    <a onClick="showMovies('seeds', '1', '');">Popular</a>
                </li>
                <li>
                    <a onClick="showMovies('rating', '1', '');">Best rated</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=action');">Action</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=adventure');">Adventure</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=animation');">Animation</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=biography');">Biography</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=comedy');">Comedy</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=crime');">Crime</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=documentary');">Documentary</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=drama');">Drama</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=family');">Family</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=fantasy');">Fantasy</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=history');">History</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=horror');">Horror</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=music');">Music</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=musical');">Musical</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=mystery');">Mystery</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=romance');">Romance</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=sci-fi');">Sci-Fi</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=sport');">Sport</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=thriller');">Thriller</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=war');">War</a>
                </li>
                <li>
                    <a onClick="showMovies('seeds', '1', '&genre=western');">Western</a>
                </li>
            </ul>
        </div>
        <div id="page-content-wrapper">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
			
	  		<div id="home">
				<a href="#menu-toggle" class="btn btn-lg btn-default" id="menu-toggle" ><span class="glyphicon glyphicon-menu-hamburger" aria-hidden="true"></span></a>
				<div id="results" ></div>
				<br>
				<nav class="pages" >
					<ul class="pagination">
						<li><a onclick="openPage('1')">1</a></li>
						<li><a onclick="openPage('2')">2</a></li>
						<li><a onclick="openPage('3')">3</a></li>
						<li><a onclick="openPage('4')">4</a></li>
						<li><a onclick="openPage('5')">5</a></li>
					</ul>
				</nav>
			</div>
			<div id="infos" style="display:none;">
		</div>
                        
                    </div>
                </div>
            </div>
        </div>

		</div>
	</body>
	<footer>
		<script src="{{get_url('static', filename='jquery-2.1.3.min.js') }}"></script>
		<script src="{{get_url('static', filename='bootstrap.min.js') }}"></script>
		<script src="{{get_url('static', filename='home.js') }}"></script>
	</footer>
	<div id="overlay"></div>
</html>
