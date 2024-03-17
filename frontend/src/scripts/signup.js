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

      console.log('Name:', name);
      console.log('Email:', email);
      console.log('Password:', password);

      // Send data to backend endpoint using jQuery Ajax
      $.ajax({
        url: 'YOUR_BACKEND_ENDPOINT_URL',
        type: 'POST',
        data: {
          name: name,
          email: email,
          password: password,
        },
        success: function (response) {
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
