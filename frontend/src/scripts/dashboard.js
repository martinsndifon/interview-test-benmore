let inputText = document.getElementById('input-text');
let closeBtn = document.getElementById('close-btn');
let projectBtn = document.getElementById('project-btn');

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

function showInfo(info) {
  let menuBtn = document.getElementById(info + '-btn');
  let content = document.getElementById('content');
  let infoContent = '';

  const menu = document.getElementById('menu');
  const buttons = menu.querySelectorAll('button');
  buttons.forEach((button) => {
    button.classList.remove('active');
  });

  menuBtn.classList.add('active');

  // Dynamically generate content based on the selected info
  switch (info) {
    case 'project':
      infoContent = '<p>The Project page test</p>';
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
