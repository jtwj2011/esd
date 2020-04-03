<?php

$username = $_POST['username'];
$password = $_POST['password'];



if ($username == 'Jose@gmail.com' && $password == 'asdfgh') {
    header("Location: homepage-tuteelogin.php");
}

if ($username=='Christopher@gmail.com' && $password =='asdfgh'){
    header("Location: homepage-tutorlogin.php");
       
}
    

