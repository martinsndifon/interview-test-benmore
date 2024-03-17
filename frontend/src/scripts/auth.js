const token = localStorage.getItem('Token');

if (token) {
  $.ajax({
    url: 'http://192.168.0.3:8000/api/user/me/',
    type: 'GET',
    headers: {
      Authorization: 'Token ' + token,
    },
    success: (response) => {
      console.log('Authenticated');
    },
    error: function (xhr, status, error) {
      window.location.href = 'signin.html';
    },
  });
} else {
  window.location.href = 'signin.html';
}
