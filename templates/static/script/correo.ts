import { Resend } from 'resend';

document.getElementById('form')?.addEventListener('submit', async function (e: Event) {
    e.preventDefault(); 

    // Capturar los datos del formulario
    const correoInput = document.getElementById('enviar') as HTMLInputElement;

    const resend = new Resend('re_Fc59PYCL_NZ7hBhitzHQePnZtZGtGvWuY');

    try {
        // Enviar los datos a la API
        const response = await fetch('/api/correo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                to:'l22020779@veracruz.tecnm.mx',
                subject: 'Código de verificación',
                html: `<p>Hola, este es tu código de verificación.</p>`,
            }),
        });

        if (response.ok) {
            alert('Correo enviado con éxito');
            // Redirigir al siguiente formulario
            window.location.href = 'vistaVerificacionCorreo.html';
        } else {
            const errorData = await response.json();
            alert(`Error al enviar el correo: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Error al enviar el correo:', error);
        alert('Ocurrió un error al enviar el correo.');
    }
});