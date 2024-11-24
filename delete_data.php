<?php
// Database configuration
$servername = "localhost";
$username = "root";
$password = "ro11@777#777";  // Replace with your MySQL password
$dbname = "contact_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the id is set in the URL
if (isset($_GET['id'])) {
    $id = intval($_GET['id']);  // Ensure the id is an integer

    // Prepare and execute the SQL statement to delete data
    $sql = "DELETE FROM contacts WHERE id=?";
    $stmt = $conn->prepare($sql);

    if ($stmt) {
        $stmt->bind_param("i", $id);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            echo "Record deleted successfully!";
        } else {
            echo "No record found with that ID.";
        }

        $stmt->close();
    } else {
        echo "Error preparing statement: " . $conn->error;
    }
} else {
    echo "ID not specified.";
}

// Close the connection
$conn->close();
?>
