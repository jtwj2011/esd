<?php

session_start();

$username = $_POST['username'];
$password = $_POST['password'];

$_SESSION['login_id'] = $username;

if ($username == 'Jose@gmail.com' && $password == 'asdfgh') {
    header("Location: homepage-tuteelogin.php");
}

if ($username=='Christopher@gmail.com' && $password =='asdfgh'){
    header("Location: homepage-tutorlogin.php");
       
}
    

