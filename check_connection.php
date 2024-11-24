<?php
// Database credentials
$servername = "localhost"; // Change this if your MySQL server is not on the same machine
$username = "root";        // Your MySQL username
$password = ""; // Your MySQL password
$database = "contact_db";  // Name of your database

// Create a connection
$conn = new mysqli($servername, $username, $password, $database);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully";

// Close the connection
$conn->close();
?>
