document.addEventListener('DOMContentLoaded', () => {
    // Código do formulário
    const form = document.getElementById('form-contato');
    const successMessage = document.getElementById('success-message');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'Accept': 'application/json' },
            });

            if (response.ok) {
                successMessage.style.display = 'block';
                form.reset();
            } else {
                alert('Ocorreu um erro. Tente novamente.');
            }
        } catch {
            alert('Erro no envio. Verifique sua conexão.');
        }
    });

    // Código do menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', String(!isExpanded));
            navLinks.classList.toggle('show');
        });
    }
});
