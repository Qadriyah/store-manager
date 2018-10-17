window.onload = () => {
  const myform = document.getElementById('myform');
  if (myform) {
    myform.addEventListener('submit', event => {
      event.preventDefault();
      const username = document.getElementById('name').value;
      const password = document.getElementById('password').value;
      if (username === 'admin' && password === 'admin') {
        window.location.href = './admin/admin-dashboard.html';
      } else {
        window.location.href = './attendant/attendant-dashboard.html';
      }
    });
  }

  const open = document.getElementById('open');
  const close = document.getElementById('close');
  if (open && close) {
    open.addEventListener('click', event => {
      openDrawer();
    });

    close.addEventListener('click', event => {
      closeDrawer();
    });
  }
};

window.addEventListener('resize', () => {
  const drawer = document.getElementById('drawer');
  if (drawer) {
    if (this.window.innerWidth > 615) {
      document.getElementById('drawer').style = 'width: 150px;';
      document.getElementById('close').style.display = 'none';
      document.getElementById('open').style.display = 'none';
    } else {
      document.getElementById('drawer').style = 'width: 0;';
      document.getElementById('open').style.display = 'block';
      document.getElementById('close').style.display = 'none';
    }
  }
});

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
