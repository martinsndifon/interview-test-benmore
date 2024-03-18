let inputText = document.getElementById('input-text');
let closeBtn = document.getElementById('close-btn');
let projectBtn = document.getElementById('project-btn');
let resultCount = document.getElementById('resultCount');

closeBtn.addEventListener('click', () => {
  inputText.value = '';
  closeBtn.style.display = 'none';
});

inputText.addEventListener('input', () => {
  if (inputText.value === '') {
    closeBtn.style.display = 'none';
  } else {
    closeBtn.style.display = 'flex';
  }
});

document.addEventListener('DOMContentLoaded', () => {
  showInfo('project');
});

function formatDate(dateString) {
  const date = new Date(dateString);
  const options = { month: 'short', day: '2-digit', year: 'numeric' };
  return date.toLocaleDateString('en-US', options);
}

function formatDuration(createdDate, dueDate) {
  const created = new Date(createdDate);
  const due = new Date(dueDate);

  // Calculate the difference in milliseconds
  const diffMs = Math.abs(due - created);

  // Convert milliseconds to days and hours
  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

  // Format the result
  let result = '';
  if (days > 0) {
    result += `${days}d`;
  }
  if (hours > 0) {
    result += `, ${hours}h`;
  }

  return result;
}

function showInfo(info) {
  let menuBtn = document.getElementById(info + '-btn');
  let content = document.getElementById('content');

  const menu = document.getElementById('menu');
  const buttons = menu.querySelectorAll('button');
  buttons.forEach((button) => {
    button.classList.remove('active');
  });

  menuBtn.classList.add('active');
  let infoContent = '';

  // Dynamically generate content based on the selected info
  switch (info) {
    case 'project':
      const token = localStorage.getItem('Token');

      if (token) {
        $.ajax({
          url: 'https://interview-test-benmore.onrender.com/api/project/',
          type: 'GET',
          headers: {
            Authorization: 'Token ' + token,
          },
          success: (res) => {
            if (res.length) {
              res.forEach((project) => {
                infoContent += `<div class="flex flex-row py-4 shadow-md rounded-lg items-center">
                <div
                  class="flex flex-row justify-center items-center gap-4 relative"
                  style="width: 40%"
                >
                  <div class="p-2 text-stone-600 absolute left-4">
                    <i class="material-icons-outlined md-18">account_circle</i>
                  </div>
                  <div class="flex flex-col gap-0">
                    <h4 class="text-sm font-semibold">${project.title}</h4>
                    <p class="text-xs font-semibold text-stone-400">${formatDate(
                      project.created_at
                    )}</p>
                  </div>
                </div>
                <div
                  class="flex bg-teal-50 text-sm font-semibold rounded-md py-2 justify-center items-center"
                  style="width: 13%"
                >
                  ${formatDuration(project.created_at, project.due_date)}
                </div>
                <div class="flex flex-col justify-center items-center" style="width: 13%">
                  <h4 class="text-sm font-semibold">90/148</h4>
                  <p class="text-xs font-semibold text-stone-400">Tasks</p>
                </div>
                <div
                  class="flex flex-col gap-0 justify-center items-center"
                  style="width: 14%"
                >
                  <div class="flex flex-row gap-1 text-sm text-blue-300">
                    <i class="material-icons-outlined md-18">linear_scale</i>Progress
                  </div>
                  <input type="range" class="status-range" title="range" />
                </div>
                <div
                  class="flex flex-row gap-2 justify-center items-center text-sm"
                  style="width: 20%"
                >
                  <div class="flex flex-row justify-between text-stone-600">
                    <i class="material-icons-outlined icon">account_circle</i>
                    <i class="material-icons-outlined icon">account_circle</i>
                    <i class="material-icons-outlined icon">account_circle</i>
                  </div>
                  <i class="material-icons-outlined md-18">more_vert</i>
                </div>
              </div>
              `;
              });
            }
            content.innerHTML = infoContent;
            resultCount.innerText = res.length;
          },
          error: function (xhr, status, error) {
            window.location.href = 'signin.html';
          },
        });
      } else {
        window.location.href = 'signin.html';
      }
      break;
    case 'task':
      infoContent = '<p>All tasks will be shown here</p>';
      content.innerHTML = infoContent;
      break;
    case 'team':
      infoContent = '<p>Feature not implemented</p>';
      content.innerHTML = infoContent;
      break;
    case 'file':
      infoContent = '<p>Feature not implemented</p>';
      content.innerHTML = infoContent;
      break;
    case 'calendar':
      infoContent = '<p>Feature not implemented</p>';
      content.innerHTML = infoContent;
      break;
    case 'inbox':
      infoContent = '<p>Feature not implemented</p>';
      content.innerHTML = infoContent;
      break;
    case 'profile':
      infoContent = '<p>Feature not implemented</p>';
      content.innerHTML = infoContent;
      break;
    default:
      infoContent = '<h2>No information found</h2>';
      content.innerHTML = infoContent;
      break;
  }
}
