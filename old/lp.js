document.getElementById('form-contato').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Mensagem enviada com sucesso! Em breve entrarei em contato.');
    this.reset();
});
