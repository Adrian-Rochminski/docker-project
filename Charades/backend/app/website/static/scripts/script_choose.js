const categories = [{
    name: 'Animals',
    icon: 'fas fa-paw'
}, {
    name: 'Celebrities',
    icon: 'fas fa-star'
}, {
    name: 'Art',
    icon: 'fas fa-palette'
}, {
    name: 'Politics',
    icon: 'fas fa-balance-scale'
}, {
    name: 'History',
    icon: 'fas fa-landmark'
}, {
    name: 'Geography',
    icon: 'fas fa-globe'
}, {
    name: 'Sports',
    icon: 'fas fa-futbol'
}, {
    name: 'Mythology',
    icon: 'fas fa-dragon'
}];

function shuffle(array) {
    let currentIndex = array.length,
        randomIndex;
    while (currentIndex !== 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
    return array;
}

function generateTiles() {
    console.log("Skrypt został załadowany poprawnie.");
    const tilesContainer = document.querySelector('.tiles');
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00',
        '#ff00ff', '#00ffff', '#c02acb'];
    const shuffledColors = shuffle(colors);
    const shuffledCategories = shuffle(categories);

    shuffledCategories.forEach((category, index) => {
            const tile = document.createElement('div');
            tile.classList.add('tile', 'col-sm-4', 'animate__animated', 'animate__fadeIn');
            tile.style.backgroundColor = shuffledColors[index % shuffledColors.length];
            tile.innerHTML = `
                <span class="tile-icon"><i class="${category.icon}"></i></span>
                <br>
                <span class="tile-text">${category.name}</span>`;
            tile.addEventListener('click', () => {
                const categoryName = category.name;
                window.location.href = `/game/${categoryName}`;
            });
            tilesContainer.appendChild(tile);

    });

}

generateTiles();