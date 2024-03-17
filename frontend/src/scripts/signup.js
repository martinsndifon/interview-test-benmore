document.addEventListener('DOMContentLoaded', function () {
  showModal();

  document
    .getElementById('signupForm')
    .addEventListener('submit', function (event) {
      event.preventDefault();

      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      if (password.length < 5) {
        alert('Password must be at least 5 characters long');
        return;
      }

      $.ajax({
        url: 'http://192.168.0.3:8000/api/user/create/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          name: name,
          email: email,
          password: password,
        }),
        success: () => {
          window.location.href = 'signin.html';
        },
        error: function (xhr, status, error) {
          console.error('Error:', error);
          alert('Failed to sign up. Please try again.');
        },
      });
    });
});

function showModal() {
  var modal = document.getElementById('signUpModal');
  modal.classList.remove('hidden');
}
