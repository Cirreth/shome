<!doctype html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Document</title>
	<style>
		body {
			background: rgb(14, 121, 126);
		}
		
		h2 {
			margin-left:5px;
			text-shadow: 4px 4px 2px rgba(50, 50, 50, 0.45);
			color: #eee;
		}
		
		input {
			margin-top: 10px;
			margin-bottom: 20px;
			margin-left: 5px;
			background: rgb(49, 155, 160);
			color: #eee;
			border: none;
			border-radius: 4px;
			width: 120px;
			height: 25px;
			-webkit-box-shadow: 4px 4px 2px 0px rgba(50, 50, 50, 0.45);
			-moz-box-shadow:    4px 4px 2px 0px rgba(50, 50, 50, 0.45);
			box-shadow:         4px 4px 2px 0px rgba(50, 50, 50, 0.45);
			outline: none;
			cursor: pointer;
		}
		
		#widgets input {
			width: 120px;
		}
		
		textarea {
		   resize: none;
		}
		
		#command {
			width: 900px;
			height: 170px;
			-webkit-box-shadow: 4px 4px 2px 0px rgba(50, 50, 50, 0.45);
			-moz-box-shadow:    4px 4px 2px 0px rgba(50, 50, 50, 0.45);
			box-shadow:         4px 4px 2px 0px rgba(50, 50, 50, 0.45);
		}
		
		#responses {
			padding-left: 3px;
			color: white;
			width: 905px;
			min-height: 300px;
			border: 1px solid #aaa;
			-webkit-box-shadow: 4px 4px 2px 0px rgba(50, 50, 50, 0.45);
			-moz-box-shadow:    4px 4px 2px 0px rgba(50, 50, 50, 0.45);
			box-shadow:         4px 4px 2px 0px rgba(50, 50, 50, 0.45);
		}
		
		.res-tbl tr td {
			border: 1px solid rgb(118, 195, 199);
		}
		
		.res-tbl tr:nth-child(odd){
			background: rgb(46, 143, 108);
		}
		
		.res-tbl tr:nth-child(even){
			background: rgb(80, 144, 168);
		}
	</style>
	<script src="/static/js/jquery-2.1.1.min.js"></script>
	<script>
		$(document).ready(function(){
			var command="null";
			$('#btn-command').click(function(){
				command = $('#command').val();
				var button = $(this);
				button.val('...');
				$.post("/command",{command: command})
					.done(function(data) {
						try {
							dt = $.parseJSON(data);
							r = '<table class="res-tbl">';
							$.each(dt, function(i,v) {
								r +='<tr>'
								if (typeof(v)=='object') {
									$.each(v, function(j, w) {
										r +='<td>'+w+'</td>'
									});
								} else {
									r +='<td>'+v+'</td>'
								}
								r +='</tr>'
							});
							r+='</table>';
							$('#responses').prepend(r+'<br/>');
						} catch (e) {
						    console.log(data.replace(/\n/gm,'<br/>'))
						    out = data.replace(/\n/gm,'<br/>');
						    out = out.replace(/[ ]/gm,'&nbsp;');
						    out = out.replace(/\t/gm,'&#9;');
							$('#responses').prepend(out+'<br/><br/>');
						}
					})
					.always(function(){
						$(button).val('Отправить');
					});
			});
			
			$('#btn-clear').click(function(){
				$('#responses').html('');
			});
			
			$('#btn-t1').click(function(){
				$('#command').val('process list');
				$('#btn-command').click();
			});
			
			$('#btn-t2').click(function(){
				$('#command').val('schedule list');
				$('#btn-command').click();
			});
			
			$('#btn-t3').click(function(){
				$('#command').val('system threads');
				$('#btn-command').click();
			});
			
		});
	</script>
</head>
<body>
	<h2>Введите команду</h2>
	<textarea id="command"></textarea><br/>
	<input type="button" id="btn-command" value="Отправить">
	<div id="widgets">
		<input type="button" id="btn-t1" value="process list">
		<input type="button" id="btn-t2" value="schedule list">
		<input type="button" id="btn-t3" value="threads">
	</div>
	<input type="button" id="btn-clear" value="Очистить">
	<div id="responses"></div>
</body>
</html>