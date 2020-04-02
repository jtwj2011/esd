<?php

$username = $_POST['username'];
$password = $_POST['password'];

$_SESSION['username'] = $username;

if ($username == 'abc@gmail.com' && $password == 'asdfgh') {
    header("Location: tutor.php");
}

if ($username=='jose@gmail.com' && $password =='asdfgh'){
    header("Location: tutee.html");
       
}
    

?>
<script>
    var name = document.getElementById("username");
    var password = document.getElementById("password");

    if name == 'jose@gmail.com' && password=='asdfgh'){
        header("Location: tutee.html");
    }
</script>