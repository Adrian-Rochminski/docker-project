const categories = [{
    name: 'Category 1',
    icon: 'fas fa-car'
}, {
    name: 'Category 2',
    icon: 'fas fa-puzzle-piece'
}, {
    name: 'Category 3',
    icon: 'fas fa-music'
}, {
    name: 'Category 4',
    icon: 'fas fa-snowflake'
}, {
    name: 'Category 5',
    icon: 'fas fa-rocket'
}, {
    name: 'Category 6',
    icon: 'fas fa-book'
}, {
    name: 'Category 7',
    icon: 'fas fa-film'
}, {
    name: 'Category 8',
    icon: 'fas fa-heart'
}, {
    name: 'Category 9',
    icon: 'fas fa-star'
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
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffffff'];
    const shuffledColors = shuffle(colors);
    const shuffledCategories = shuffle(categories);
    shuffledCategories.forEach((category, index) => {
        const tile = document.createElement('div');
        tile.classList.add('tile', 'col-md-4', 'animate__animated', 'animate__fadeIn');
        tile.style.backgroundColor = shuffledColors[index];
        tile.innerHTML = `
            <span class="tile-icon"><i class="${category.icon}"></i></span>
            <br>
            <span class="tile-text">${category.name}</span>`;
        tilesContainer.appendChild(tile);
    });
       tile.addEventListener('click', () => {
            const categoryName = category.name;
            $.ajax({
                url: '/your-backend-endpoint',
                type: 'POST',
                data: {
                    categoryName: categoryName
                },
                success: function(response) {
                    console.log(response);
                }
            });
        });
}

generateTiles();
