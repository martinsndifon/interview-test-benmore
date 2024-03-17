document.addEventListener('DOMContentLoaded', function () {
  showModal();

  document
    .getElementById('signinForm')
    .addEventListener('submit', function (event) {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      $.ajax({
        url: 'http://192.168.0.3:8000/api/user/token/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ email: email, password: password }),
        success: (data) => {
          localStorage.setItem('Token', data.token);
          window.location.href = 'dashboard.html';
        },
        error: function (xhr, status, error) {
          console.error('Error:', error);
          alert('Failed to sign in. Please try again.');
        },
      });
    });
});

function showModal() {
  let modal = document.getElementById('signInModal');
  modal.classList.remove('hidden');
}
