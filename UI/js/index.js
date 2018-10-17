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
      openDrawer({
        style: 'width: 150px; position: absolute; top: 10px; z-index: 1;',
        open: 'none',
        close: 'block'
      });
    });

    close.addEventListener('click', event => {
      openDrawer({
        style: 'width: 0;',
        open: 'block',
        close: 'none'
      });
    });
  }
};

window.addEventListener('resize', () => {
  const drawer = document.getElementById('drawer');
  if (drawer) {
    if (this.window.innerWidth > 615) {
      openDrawer({
        style: 'width: 150px;',
        open: 'none',
        close: 'none'
      });
    } else {
      openDrawer({
        style: 'width: 0;',
        open: 'block',
        close: 'none'
      });
    }
  }
});

openDrawer = options => {
  document.getElementById('drawer').style = options.style;
  document.getElementById('open').style.display = options.open;
  document.getElementById('close').style.display = options.close;
};
