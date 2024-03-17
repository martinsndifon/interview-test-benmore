document.addEventListener('DOMContentLoaded', function () {
  showModal();

  document
    .getElementById('signinForm')
    .addEventListener('submit', function (event) {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      console.log('Email:', email);
      console.log('Password:', password);
    });
});

function showModal() {
  let modal = document.getElementById('signInModal');
  modal.classList.remove('hidden');
}
