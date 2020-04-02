<?php

$username = $_POST['username'];
$password = $_POST['password'];

echo"$username";
echo"$password";


if ($username == 'abc@gmail.com' && $password == 'asdfgh') {
    header("Location: tutor.html");
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