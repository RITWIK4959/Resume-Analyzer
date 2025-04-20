<?php
session_start();

// Check if user is logged in
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    header("Location: login.html");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            min-height: 100vh;
            background: #F3F4F6;
        }

        .header {
            background: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 24px;
        }

        .back-button {
            background: #DC3545;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            transition: background-color 0.2s;
        }

        .back-button:hover {
            background: #C82333;
        }

        .welcome-text {
            color: #1F2937;
            font-size: 24px;
            font-weight: 500;
        }

        .logout-btn {
            background: #DC3545;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            transition: background-color 0.2s;
        }

        .logout-btn:hover {
            background: #C82333;
        }

        .container {
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
        }

        .card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1.5rem;
        }

        .card-icon {
            color: #3B82F6;
            font-size: 2.5rem;
        }

        .card-title {
            color: #1F2937;
            font-size: 1.5rem;
            font-weight: 500;
        }

        .card-description {
            color: #6B7280;
            font-size: 1rem;
            line-height: 1.5;
        }

        .card-button {
            background: #3B82F6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            transition: background-color 0.2s;
        }

        .card-button:hover {
            background: #2563EB;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-left">
            <h1 class="welcome-text">Welcome, <?php echo htmlspecialchars($_SESSION['username']); ?>!</h1>
        </div>
        <a href="logout.php" class="logout-btn">
            <i class="fas fa-sign-out-alt"></i>
            Logout
        </a>
    </header>

    <div class="container">
        <div class="card">
            <i class="fas fa-file-alt card-icon"></i>
            <h2 class="card-title">Resume Analyzer</h2>
            <p class="card-description">
                Analyze and evaluate resumes using our advanced AI-powered tools. 
                Get detailed insights and recommendations.
            </p>
            <a href="analyzer.html" class="card-button">
                <i class="fas fa-chart-line"></i>
                GO TO ANALYZER
            </a>
        </div>

        <div class="card">
            <i class="fas fa-book card-icon"></i>
            <h2 class="card-title">Sample Resumes</h2>
            <p class="card-description">
                Browse through our collection of professional resume examples 
                and templates for inspiration.
            </p>
            <a href="samples.html" class="card-button">
                <i class="fas fa-eye"></i>
                VIEW SAMPLES
            </a>
        </div>
    </div>
</body>
</html> 