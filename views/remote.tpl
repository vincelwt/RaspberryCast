<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8">
		<meta charset="utf-8">
		<title>RaspberryCast</title>
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
		<link href="{{get_url('static', filename='remote.css') }}" rel="stylesheet">
		<link href="{{get_url('static', filename='bootstrap.min.css') }}" rel="stylesheet">
		<link rel="icon" type="image/png" sizes="192x192" href="{{get_url('static', filename='favicon.png') }}" />
	</head>
	<body>
		<center>
		<div id="whole">
				
				<div id="message"></div>			
				
				<form id="stream_form" class="form-inline">
						<div class="input-group">
							<input type="search" class="form-control input-lg" id="media_url" placeholder="Media's URL" aria-hidden="true">
							<span id="clear_search" class="glyphicon glyphicon-remove-circle"></span>
						</div>
						<br>
						<br>
						<div>
							<button id="castbtn" class="btn btn-lg btn-success fifty" title="Cast now" type="button">Cast<span class="glyphicon glyphicon-send pull-right" aria-hidden="true"></button>
							<button id="addqueue" title="Add current video to queue" class="btn btn-lg btn-info fifty" type="button">Queue<span class="glyphicon glyphicon-menu-hamburger pull-right" aria-hidden="true" ></button>
						</div>
				</form>
				<div>
					<button id="pause" type="button" title="Play/pause" class="fifty btn btn-info">
						<span class="glyphicon glyphicon-play" aria-hidden="true"></span>
						<span class="glyphicon glyphicon-pause" aria-hidden="true"></span>
					</button>
					<button id="stop" type="button" title="Stop video/Next queue video" class="fifty btn btn-danger">
						<span class="glyphicon glyphicon-stop" aria-hidden="true"></span>
					</button>
				</div>
				<div>
					<button id="backward" type="button" title="Backward" class="fifty btn btn-warning">
						<span class="glyphicon glyphicon-backward" aria-hidden="true"></span><span class="tb"> -30s</span>
					</button>
					<button id="forward" type="button" title="Forward" class="fifty btn btn-warning">
						<span class="tb">+30s </span><span class="glyphicon glyphicon-forward" aria-hidden="true"></span>
					</button>
				</div>
				<div>
					<button id="vol_down" type="button" title="Volume -" class="fifty btn btn-primary">
						<span class="glyphicon glyphicon-volume-down" aria-hidden="true"></span>
					</button>
					<button id="vol_up" type="button" title="Volume +" class="fifty btn btn-primary">
						<span class="glyphicon glyphicon-volume-up" aria-hidden="true"></span>
					</button>
				</div>
				<br>
				<a id="link-text" onClick="advanced()">More options ▾</a>
				<div id="advanced" style="display:none">
					<form id="shut_form" class="form-inline">
						<div class="form-group">
							<div class="input-group">
								<input type="number" class="form-control input-lg" id="time_shut" placeholder="Delayed shutdown (minutes)" pattern="\d*" min="0" max="400" step="5">
								<div class="input-group-btn"><button id="shutbtn" class="btn btn-lg btn-info form_button" type="button"><span class="glyphicon glyphicon-time" aria-hidden="true"></button></div>
							</div>
						</div>
					</form>
					<div>
						<button id="cancelshut" type="button" title="Cancel shutdown" class="fifty btn btn-danger">
							<span class="tb">Cancel shutdown </span><span class="glyphicon glyphicon-remove-circle pull-left" aria-hidden="true"></span>
						</button>
						<button id="nextqueue" type="button" title="Next video in playlist" class="fifty btn btn-primary">
							<span class="tb">Next video </span><span class="glyphicon glyphicon-step-forward pull-right" aria-hidden="true"></span>
						</button>
					</div>
					<div>
						<button id="long-backward" type="button" title="Long skip backwards" class="fifty btn btn-info">
							<span class="tb">
								<span class="glyphicon glyphicon-backward  pull-left" aria-hidden="true"></span>
								-10 minutes
							</span>
						</button>
						<button id="long-forward" type="button" title="Long skip backwards" class="fifty btn btn-info">
							<span class="tb">+10 minutes
								<span class="glyphicon glyphicon-forward pull-right" aria-hidden="true"></span>
							</span>
						</button>
					</div>
					<!-- History and playlist management -->
					<div id="last-div">
						<button id="history-button" onClick="showHistory()" type="button" title="History" class="ninety btn btn-warning">
							<span class="tb">
								<span class="glyphicon glyphicon-list-alt  pull-left" aria-hidden="true"></span>
								History
							</span>
						</button>
					</div>
					<div id="history-div" style="display:none">
					</div>
				</div>
			
		</div>
		</center>
		

		<!-- script references -->
		
		<script src="{{get_url('static', filename='jquery-2.1.3.min.js') }}"></script>
		<script src="{{get_url('static', filename='history.js') }}"></script>
		<script src="{{get_url('static', filename='remote.js') }}"></script>
	</body>
</html>
