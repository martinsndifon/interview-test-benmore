document.addEventListener('DOMContentLoaded', function () {
  const openModalButton = document.getElementById('openProjectModalBtn');
  const closeModalButton = document.getElementById('closeProjectModalBtn');
  const modal = document.getElementById('newProjectModal');
  const submitProjectBtn = document.getElementById('submitProjectBtn');

  openModalButton.onclick = function () {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
  };

  closeModalButton.onclick = function () {
    modal.classList.remove('flex');
    modal.classList.add('hidden');
  };

  window.onclick = function (event) {
    if (event.target === modal) {
      modal.classList.remove('flex');
      modal.classList.add('hidden');
    }
  };

  const myForm = document.getElementById('newProjectForm');
  myForm.addEventListener('submit', function (event) {
    event.preventDefault();
    submitProjectBtn.disabled = true;

    const formData = new FormData(myForm);

    const title = formData.get('title');
    const description = formData.get('description');
    const dueDate = formData.get('dueDate');

    const token = localStorage.getItem('Token');

    if (token) {
      $.ajax({
        url: 'https://interview-test-benmore.onrender.com/api/project/',
        type: 'POST',
        contentType: 'application/json',
        headers: {
          Authorization: 'Token ' + token,
        },
        data: JSON.stringify({
          title: title,
          description: description,
          due_date: dueDate,
        }),
        success: () => {
          location.reload();
          console.log('success');
        },
        error: function (xhr, status, error) {
          console.error('Error:', error);
          submitProjectBtn.disabled = false;
          alert('Failed to create property. Please try again.');
        },
      });
    } else {
      window.location.href = 'signin.html';
    }
  });
});
