const container = document.querySelector('.container');
        const registerBtn = document.querySelector('.register-btn');
        const loginBtn = document.querySelector('.login-btn');

        registerBtn.addEventListener('click', () => {
            container.classList.add('active');
            history.pushState(null, '', '/register'); // change URL without reload
        });
      
        loginBtn.addEventListener('click', () => {
            container.classList.remove('active');
            history.pushState(null, '', '/login');
        });