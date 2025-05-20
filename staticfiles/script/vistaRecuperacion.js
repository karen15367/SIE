// JavaScript para mostrar/ocultar contraseña
        document.addEventListener('DOMContentLoaded', function () {
            // Para el primer campo de contraseña
            const togglePassword = document.querySelector('#togglePassword');
            const password = document.querySelector('#password');

            togglePassword.addEventListener('click', function () {
                // Alternar  el tipo de entrada entre "password" y "text"
                const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
                password.setAttribute('type', type);

                // Alternar el icono entre ojo y ojo tachado
                this.classList.toggle('fa-eye');
                this.classList.toggle('fa-eye-slash');
            });

            // Para el campo de confirmar contraseña
            const toggleConfirmPassword = document.querySelector('#toggleConfirmPassword');
            const confirmPassword = document.querySelector('#confirmPassword');

            toggleConfirmPassword.addEventListener('click', function () {
                // Alternar el tipo de entrada entre "password" y "text"
                const type = confirmPassword.getAttribute('type') === 'password' ? 'text' : 'password';
                confirmPassword.setAttribute('type', type);

                // Alternar el icono entre ojo y ojo tachado
                this.classList.toggle('fa-eye');
                this.classList.toggle('fa-eye-slash');
            });
        });
        // JavaScript para establecer la fecha máxima en el campo de fecha de nacimiento
        document.addEventListener('DOMContentLoaded', function () {
            const fechaNacimientoInput = document.getElementById('fechaNacimiento');
            const today = new Date().toISOString().split('T')[0];
            fechaNacimientoInput.setAttribute('max', today);
        });


        //validar ambas pwd
        document.addEventListener('DOMContentLoaded', function () {
        const form = document.getElementById('recuperar');
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirmPassword');

        form.addEventListener('submit', function (event) {
            if (password.value !== confirmPassword.value) {
                event.preventDefault(); // Evita que el formulario se envíe
                alert('Las contraseñas no coinciden. Por favor, verifica e inténtalo de nuevo.');
            }
        });
    });