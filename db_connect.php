<?php
$servername = "%localhost";  // Your MySQL server name or IP address
$username = "root";         // Your MySQL username
$password = ""; // Your MySQL password
$dbname = "contact_db";     // Your MySQL database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";
?>
