document.addEventListener('DOMContentLoaded', function () {
  const submitBtn = document.getElementById('submitBtn');
  showModal();

  document
    .getElementById('signupForm')
    .addEventListener('submit', function (event) {
      event.preventDefault();
      submitBtn.disabled = true;

      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      if (password.length < 5) {
        alert('Password must be at least 5 characters long');
        submitBtn.disabled = false;
        return;
      }

      $.ajax({
        url: 'https://interview-test-benmore.onrender.com/api/user/create/',
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
          submitBtn.disabled = false;
          alert('Failed to sign up. Please try again.');
        },
      });
    });
});

function showModal() {
  var modal = document.getElementById('signUpModal');
  modal.classList.remove('hidden');
}
