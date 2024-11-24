<?php
include 'db_connect.php'; // Include the database connection file

$sql = "SELECT * FROM contacts";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Output data of each row
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"]. " - Name: " . $row["name"]. " - Email: " . $row["email"]. " - Phone: " . $row["phone"]. " - Message: " . $row["message"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>
