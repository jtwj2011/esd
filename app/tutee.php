<?php
$username=$_POST['username'];

?>
<html>

<head>
   
    
    
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width">

    

    <!-----CSS CODE LINKS-->
    <link href="css/bootstrap.min1.css" rel="stylesheet">
    <link href="css/font-awesome.min1.css" rel="stylesheet">
    <link href="css/styles3.css" rel="stylesheet">

    
        <link rel="stylesheet" type="text/css" href="css/perfect-scrollbar.css">
    <!--===============================================================================================-->
        <link rel="stylesheet" type="text/css" href="css/util.css">
        <link rel="stylesheet" type="text/css" href="css/main.css">
    <!--===============================================================================================-->
    

    <!-- Latest compiled and minified JavaScript -->
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script 
    src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    
    <script
    src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"
    integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut"
    crossorigin="anonymous"></script>
    
    <script 
    src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"
    integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k"
    crossorigin="anonymous"></script>
    
    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    
    
</head>

<body>

    <nav class="navbar navbar-custom navbar-fixed-top">
        <div class="container-fluid">
            <div class="navbar-header">
                <div class="site-title">
                    <i class="fa fa-book" style="font-size:60px;color:white" ></i>
                    <h4>Expert Home Tutors</h4>
                </div>
            </div>
        </div>
    </nav>
    <div id="sidebar-collapse" class="col-sm-2 sidebar">
        <div class="profile-sidebar">
            <div class="profile-userpic">
                <img src="image/face.jpeg" class="img-responsive">
            </div>
            <div class="profile-usertitle">
                <div class="profile-usertitle-name"><?= $username ?></div>
                <div class="profile-usertitle-status">Online</div>
            </div>
            <div class="clear"></div>
        </div>
        <ul class="nav menu">
            <li class="active"><a href="tutee.html"><em class="fa fa-user-circle">&nbsp;</em> Find Tutors</a></li>
            <li><a href="bidding.php"><em class="fa fa-pencil">&nbsp;</em> Profile</a></li>
            <li><a href="logout.php"><em class="fa fa-power-off">&nbsp;</em> Logout</a></li>
        </ul>
    </div>

    <div class="col-sm-10 col-sm-offset-2 main">
        <div class="row">
            <ol class="breadcrumb">
                <li><a href="#">
                        <em class="fa fa-user-circle"></em>
                    </a></li>
                <li class="active">Find Tutors</li>
            </ol>
        </div>
              
        
        
        <div class="row">
			<div class="col-md-12">
				<div class="panel panel-default">
					<div class="panel-body">

<div class="limiter">
    <div class="container-table100">
        <div class="wrap-table100">
        <div class="table100 ver3 m-b-110">
                <div class="table100-head">
                    <div class="table100-body js-pscroll">
                    <table id="tutorsTable" >
                        <thead>
                            <tr>
                                <th class="cell100 column2">Name</th>
                                <th class="cell100 column2">Gender</th>
                                <th class="cell100 column2">Level</th>
                                <th class="cell100 column2">Subject</th>
                                <th class="cell100 column2">Subject Rate</th>
                                <th class="cell100 column2">Review</th>
                                
                            </tr>
                        </thead>
            </table>
            <br>
            <h3 id="errors"></h3>
        </div>
    
        <script>
            
    
                $(async() => {           
                    var serviceURL = "http://127.0.0.1:5001/tutor";
            
                    try {
                        const response =
                        await fetch(
                        serviceURL, { method: 'GET' }
                        );
                        const data = await response.json();
                        var tutors = data.Tutor;
                        console.log(tutors);
                        // console.log(!tutors);
                        // console.log(tutors.length);
    
            
                        if (!tutors || !tutors.length) {
                            showError('No tutors.')
                        } else {
                            var rows = "";
                            // console.log(tutors);
                            for (const tutor of tutors) {
                                // console.log(tutor);
                                eachRow = 
                                    "<td><a href='logout.php'>" + tutor.name + "</td>" +
                                    "<td>" + tutor.gender + "</td>" +
                                    "<td>" + tutor.level + "</td>" +
                                    "<td>" + tutor.subject + "</td>" +
                                    "<td>" + tutor.subject_rate + "</td>" +
                                    "<td>"+"<a href='http://localhost:5000/tutee/request/"+tutor.tutor_id+"/"+tutor.subject+ "'>" + "Button" +  "</a></td>";
                                
                                    
                                // console.log(eachRow);
                                rows += "<tr>" + eachRow + "</tr>";
                                console.log(rows);
                            }
                            // console.log(book);
                            $('#tutorsTable').append(rows);
                        }
                    } catch (error) {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    // showError
                    // ('There is a problem retrieving the book data, please try again later.<br />'+error);
                    }
                });
            // });
        </script>
                    
          </div>             
<div class="limiter">
    <div class="container-table100">
        <div class="wrap-table100">
                   
      
         
  
</style>
</head>


</body>
</html>

</body>


<!--===============================================================================================-->	
<script src="js/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="js/popper.js"></script>
	<script src="js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="js/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="js/perfect-scrollbar.min.js"></script>
	<script>
		$('.js-pscroll').each(function(){
			var ps = new PerfectScrollbar(this);

			$(window).on('resize', function(){
				ps.update();
			})
		});
			
		
	</script>
<!--===============================================================================================-->
	<script src="js/main.js"></script>
</html>
