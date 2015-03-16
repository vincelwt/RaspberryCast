<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8">
		<meta charset="utf-8">
		<title>RaspberryCast</title>
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
		<link href="{{get_url('static', filename='style.css') }}" rel="stylesheet">
		<link href="{{get_url('static', filename='bootstrap.min.css') }}" rel="stylesheet">
	</head>
	<body>
		<center>
		<div id="whole">
			
				
				<form id="stream_form" class="form-inline">
					<div class="form-group">
						<div class="input-group">
							<input type="text" class="form-control input-lg" id="media_url" placeholder="Media's URL">
							<div class="input-group-btn"><button id="castbtn" class="btn btn-lg btn-danger form_button" type="button"><span class="glyphicon glyphicon-send" aria-hidden="true"></button></div>
						</div>
					</div>
				</form>
				
				<div>
					<button id="addqueue" title="Add current video to queue" type="button" class="fifty btn btn-primary">
						<span class="glyphicon glyphicon-list" aria-hidden="true"></span>
					</button>
					<button id="remqueue" title="Empty queue" type="button" class="fifty btn btn-primary">
						<span class="glyphicon glyphicon-trash" aria-hidden="true"></a></span>
					</button>
				</div>
				<div>
					<button id="pause" type="button" title="Play/pause" class="fifty btn btn-info">
						<span class="glyphicon glyphicon-pause" aria-hidden="true"></span>
					</button>
					<button id="stop" type="button" title="Stop video/Next queue video" class="fifty btn btn-danger">
						<span class="glyphicon glyphicon-stop" aria-hidden="true"></a></span>
					</button>
				</div>
				<div>
					<button id="backward" type="button" title="Backward" class="fifty btn btn-warning">
						<span class="glyphicon glyphicon-backward" aria-hidden="true"></a></span>
					</button>
					<button id="forward" type="button" title="Forward" class="fifty btn btn-warning">
						<span class="glyphicon glyphicon-forward" aria-hidden="true"></a></span>
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
			
			
		</div>
		</center>
		<div id="popalert" style="display:none">
		</div>

		<!-- script references -->
		
		<script src="{{get_url('static', filename='jquery-2.1.3.min.js') }}"></script>
		<script src="{{get_url('static', filename='script.js') }}"></script>
	</body>
</html>
