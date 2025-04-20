function logout() {
    fetch('logout.php')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                localStorage.removeItem('isLoggedIn');
                window.location.href = 'login.html';
            }
        })
        .catch(error => console.error('Error:', error));
}
