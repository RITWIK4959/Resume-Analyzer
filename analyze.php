<?php
require 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_FILES['resume']) || !isset($_POST['jobDescription'])) {
        echo json_encode(["success" => false, "message" => "Missing data"]);
        exit;
    }

    if (!file_exists('uploads')) {
        mkdir('uploads', 0777, true);
    }

    $resumePath = 'uploads/' . basename($_FILES['resume']['name']);

    if (!move_uploaded_file($_FILES['resume']['tmp_name'], $resumePath)) {
        echo json_encode(["success" => false, "message" => "Failed to save uploaded file"]);
        exit;
    }

    $jobDescription = $_POST['jobDescription'];

    $flaskUrl = "http://127.0.0.1:5000/analyze";

    $curl = curl_init($flaskUrl);
    $postData = [
        'resume' => new CURLFile($resumePath),
        'jobDescription' => $jobDescription
    ];

    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $postData);

    $response = curl_exec($curl);

    if ($response === false) {
        echo json_encode(["success" => false, "message" => "Error contacting AI server"]);
        exit;
    }

    curl_close($curl);

    echo $response;
}
?>
