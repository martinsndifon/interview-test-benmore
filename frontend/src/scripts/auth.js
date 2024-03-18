const token = localStorage.getItem('Token');

if (token) {
  $.ajax({
    url: 'https://interview-test-benmore.onrender.com/api/user/me/',
    type: 'GET',
    headers: {
      Authorization: 'Token ' + token,
    },
    success: (response) => {},
    error: function (xhr, status, error) {
      window.location.href = 'signin.html';
    },
  });
} else {
  window.location.href = 'signin.html';
}
