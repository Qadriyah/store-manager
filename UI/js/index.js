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
