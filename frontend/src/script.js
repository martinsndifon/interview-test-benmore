let inputText = document.getElementById('input-text');
let closeBtn = document.getElementById('close-btn');

closeBtn.addEventListener('click', () => {
  inputText.value = '';
  closeBtn.style.display = 'none';
});

inputText.addEventListener('input', () => {
  if (inputText.value === '') {
    closeBtn.style.display = 'none';
  } else {
    closeBtn.style.display = 'block';
  }
});

document.addEventListener('DOMContentLoaded', () => {
  showInfo('project');
});

function showInfo(info) {
  let content = document.getElementById('content');

  let infoContent = '';

  // Dynamically generate content based on the selected info
  switch (info) {
    case 'project':
      infoContent = '<p>The Project page</p>';
      break;
    case 'task':
      infoContent = '<p>All tasks will be shown here</p>';
      break;
    case 'team':
      infoContent = '<p>Feature not implemented</p>';
      break;
    case 'file':
      infoContent = '<p>Feature not implemented</p>';
      break;
    case 'calendar':
      infoContent = '<p>Feature not implemented</p>';
      break;
    case 'inbox':
      infoContent = '<p>Feature not implemented</p>';
      break;
    case 'profile':
      infoContent = '<p>Feature not implemented</p>';
      break;
    default:
      infoContent = '<h2>No information found</h2>';
      break;
  }

  content.innerHTML = infoContent;
}
