// onsubmit event handler
onSubmit = () => {
  const name = document.getElementById('name').value;
  const password = document.getElementById('password').value;
  if (name.length === 0) {
    alert('Username is required');
    return false;
  }
  if (password.length === 0) {
    alert('Password is required');
    return false;
  }
};

openDrawer = () => {
  document.getElementById('drawer').style =
    'width: 150px; position: absolute; top: 10px; z-index: 1;';
  document.getElementById('open').style.display = 'none';
  document.getElementById('close').style.display = 'block';
};

closeDrawer = () => {
  document.getElementById('drawer').style = 'width: 0;';
  document.getElementById('close').style.display = 'none';
  document.getElementById('open').style.display = 'block';
};

window.addEventListener('resize', () => {
  if (this.window.innerWidth > 615) {
    document.getElementById('drawer').style = 'width: 150px;';
    document.getElementById('close').style.display = 'none';
    document.getElementById('open').style.display = 'none';
  } else {
    document.getElementById('drawer').style = 'width: 0;';
    document.getElementById('open').style.display = 'block';
    document.getElementById('close').style.display = 'none';
  }
});
