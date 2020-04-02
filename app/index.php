<?php

$username = $_POST['username'];
$password = $_POST['password'];
$userid = $_SESSION['user'];
echo"$username";
echo"$password";


if ($username == 'abc@gmail.com' && $password == 'asdfgh') {
    header("Location: tutor.html");
}

if ($username=='jose@gmail.com' && $password =='asdfgh'){
    header("Location: tutee.html");
       
}
    

?>