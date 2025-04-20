<?php
require 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    // Validate password
    if (strlen($password) < 8) {
        http_response_code(400);
        echo "Password must be at least 8 characters long.";
        exit();
    }

    if (!preg_match("/[A-Z]/", $password)) {
        http_response_code(400);
        echo "Password must contain at least one uppercase letter.";
        exit();
    }

    if (!preg_match("/[a-z]/", $password)) {
        http_response_code(400);
        echo "Password must contain at least one lowercase letter.";
        exit();
    }

    if (!preg_match("/[0-9]/", $password)) {
        http_response_code(400);
        echo "Password must contain at least one number.";
        exit();
    }

    if (!preg_match("/[!@#$%^&*()\-_=+{};:,<.>]/", $password)) {
        http_response_code(400);
        echo "Password must contain at least one special character.";
        exit();
    }

    // First check if username already exists
    $checkStmt = $pdo->prepare("SELECT username FROM users WHERE username = ?");
    $checkStmt->execute([$username]);
    
    if ($checkStmt->rowCount() > 0) {
        http_response_code(400); // Set error status code
        echo "Username already exists. Please choose a different username.";
        exit();
    }

    // If username doesn't exist, proceed with insertion
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
    $stmt = $pdo->prepare("INSERT INTO users (username, password) VALUES (?, ?)");

    try {
        $stmt->execute([$username, $hashedPassword]);
        header("Location: login.html");
        exit();
    } catch (PDOException $e) {
        http_response_code(400);
        echo "An error occurred. Please try again.";
    }
}
?>
