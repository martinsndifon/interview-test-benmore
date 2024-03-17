const token = localStorage.getItem('Token');

if (token) {
  // Send request to endpoint to get user data
  $.ajax({
    url: 'https://your-backend-api.com/user',
    type: 'GET',
    headers: {
      Authorization: 'Token ' + token,
    },
    success: (response) => {
      // User is authenticated, redirect to dashboard
      window.location.href = 'dashboard.html';
    },
    error: function (xhr, status, error) {
      // Token is invalid or expired, redirect to sign-in page
      window.location.href = 'signin.html';
    },
  });
} else {
  // No token found, redirect to sign-in page
  window.location.href = 'signin.html';
}
