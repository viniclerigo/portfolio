const images = [
    './img/chevette01.jpg',
    './img/chevette02.jpg',
    './img/batalha01.jpg',
    './img/batalha02.jpg',
    './img/chevette03.jpg',
    './img/chevette04.jpg',
];

let currentImageIndex = 0;

const imgElement = document.getElementById('carro-img');
const prevButton = document.getElementById('prev-btn');
const nextButton = document.getElementById('next-btn');

function showImage(index) {
    if (index < 0) {
        currentImageIndex = images.length - 1;
    } else if (index >= images.length) {
        currentImageIndex = 0;
    } else {
        currentImageIndex = index;
    }
    imgElement.src = images[currentImageIndex];
}

prevButton.addEventListener('click', () => {
    showImage(currentImageIndex - 1);
});

nextButton.addEventListener('click', () => {
    showImage(currentImageIndex + 1);
});

// Inicia com a primeira imagem
showImage(currentImageIndex);
