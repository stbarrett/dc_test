<?php

	if($_SERVER['REQUEST_METHOD'] == 'POST'):
	
		$email = $_POST['email'];
		$hasError = false;
		if(!isValidEmail($email)) { $hasError = true; } else {

			/* Open Wordpress Connection */
			$mysqli_wp = new mysqli('internal-db.s57895.gridserver.com', 'db57895_diz', 'Da5th!Vad35', 'db57895_dizcollect');
			$tm = $_SERVER['REQUEST_TIME'];
			$tm = date("Y-m-d H:i:s", $tm);
			$qry = 'INSERT INTO launch_emails (email, added) VALUES ("'.$mysqli_wp->real_escape_string($email).'", "'.$tm.'")';
			$mysqli_wp->query($qry);
			
			echo $mysqli_wp->error;
			$mysqli_wp->close();			
		}
	endif;

	function isValidEmail($email){
		return eregi("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$", $email);
	}

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <title>Dizcollect.com - Track and Share your Disney Collection Today!</title>
<style type="text/css">
html { margin:0; padding:0; width:100%;}
body { margin:0; padding:0; width:100%; font-family:arial;}
.error { color:#f00; font-weight:bold; display:block;}
#main-container {
	background: url('back.png') top left no-repeat;
	width:898px;
	height:800px;
	margin: 0 auto;
	position:relative;
}

#main-container-t {
	background: url('thanks.png') top left no-repeat;
	width:898px;
	height:800px;
	margin: 0 auto;
	position:relative;
}

#email {
	position:absolute;
	left:170px; top:503px;
	width:350px; height:25px;
	font-size:20px; color:#000;
	border:none; background:none;
}

#signup {
	position:absolute;
	left:560px; top:494px;
}

#email-msg {
	position:absolute;
	left:160px; top:545px;
}


</style>
<script type="text/javascript">
window.onload = function() {
  document.getElementById("email").focus();
};

</script>
</head>
<body>
<?php if($_SERVER['REQUEST_METHOD'] == 'POST' && !$hasError):?>
	<div id="main-container-t">
		
	</div>
<?php else: ?>
	<div id="main-container">
		<form id="subscribe" method="post">
			<input type="text" id="email" value="<?php echo $email; ?>" name="email" />
			<input type="image" src="signup.png" alt="Sign Up" border="0" id="signup" style="outline:none" />
		</form>
		<div id="email-msg">
		<?php if($hasError): ?><span class="error">Please Enter A Valid Email Address</span><br /><?php endif; ?>
		<img src="email.png" alt="" />
		</div>
	</div>
<?php endif; ?>
</body>
</html>