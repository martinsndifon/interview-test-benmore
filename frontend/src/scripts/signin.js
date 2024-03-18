document.addEventListener('DOMContentLoaded', function () {
  const submitBtn = document.getElementById('submitBtn');
  showModal();

  document
    .getElementById('signinForm')
    .addEventListener('submit', function (event) {
      event.preventDefault();
      submitBtn.disabled = true;
      console.log('reached');

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      $.ajax({
        url: 'https://interview-test-benmore.onrender.com/api/user/token/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ email: email, password: password }),
        success: (data) => {
          localStorage.setItem('Token', data.token);
          window.location.href = 'dashboard.html';
        },
        error: function (xhr, status, error) {
          console.error('Error:', error);
          submitBtn.disabled = false;
          alert('Failed to sign in. Please try again.');
        },
      });
    });
});

function showModal() {
  let modal = document.getElementById('signInModal');
  modal.classList.remove('hidden');
}
