<?php
session_start();
require 'config.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    // Validate input
    if (empty($username) || empty($password)) {
        http_response_code(400);
        echo json_encode(['error' => 'Please fill in all fields']);
        exit();
    }

    try {
        // Check if user exists
        $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
        $stmt->execute([$username]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password'])) {
            // Valid credentials - set session variables
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            $_SESSION['logged_in'] = true;

            // Redirect to dashboard
            header("Location: dashboard.php");
            exit();
        } else {
            // Invalid credentials
            http_response_code(401);
            echo "Invalid username or password";
            exit();
        }
    } catch (PDOException $e) {
        // Database error
        http_response_code(500);
        echo "An error occurred. Please try again.";
        exit();
    }
} else {
    // Invalid request method
    http_response_code(405);
    echo json_encode(['error' => 'Invalid request method']);
    exit();
}
?>
