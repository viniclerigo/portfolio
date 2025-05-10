document.addEventListener("DOMContentLoaded", function () {
    const leftArrow = document.querySelector('.arrow.left');
    const rightArrow = document.querySelector('.arrow.right');
    const images = document.querySelectorAll('.gallery-frame img');
    let activeIndex = 0; // Índice da imagem ativa

    // Função para mostrar a imagem com base no índice
    function updateActiveImage() {
        images.forEach((img, index) => {
            img.classList.remove('active'); // Remove a classe active de todas as imagens
            if (index === activeIndex) {
                img.classList.add('active'); // Adiciona a classe active na imagem atual
            }
        });
    }

    // Evento para a seta da esquerda
    leftArrow.addEventListener('click', function () {
        activeIndex = (activeIndex === 0) ? images.length - 1 : activeIndex - 1; // Vai para a imagem anterior
        updateActiveImage();
    });

    // Evento para a seta da direita
    rightArrow.addEventListener('click', function () {
        activeIndex = (activeIndex === images.length - 1) ? 0 : activeIndex + 1; // Vai para a próxima imagem
        updateActiveImage();
    });

    // Inicializa a imagem ativa na primeira carga
    updateActiveImage();
});

// Seletor das imagens da galeria
const galleryImages = document.querySelectorAll('.gallery-frame img');
const popup = document.getElementById('image-popup');
const popupImage = document.getElementById('popup-image');
const closeBtn = document.querySelector('.close-btn');
const popupLeft = document.querySelector('.popup-arrow.left');
const popupRight = document.querySelector('.popup-arrow.right');

let currentIndex = 0;

// Abrir popup ao clicar na imagem
galleryImages.forEach((img, index) => {
    img.addEventListener('click', () => {
        popup.classList.remove('hidden');
        popupImage.src = img.src;
        currentIndex = index;
    });
});

// Fechar popup
closeBtn.addEventListener('click', () => {
    popup.classList.add('hidden');
});

// Alternar imagem no popup
popupLeft.addEventListener('click', () => {
    currentIndex = (currentIndex === 0) ? galleryImages.length - 1 : currentIndex - 1;
    popupImage.src = galleryImages[currentIndex].src;
});

popupRight.addEventListener('click', () => {
    currentIndex = (currentIndex === galleryImages.length - 1) ? 0 : currentIndex + 1;
    popupImage.src = galleryImages[currentIndex].src;
});
