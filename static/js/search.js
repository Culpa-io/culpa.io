var latestQuery = null;
var focus_categories = [];

function updateView(core_response) {
    const { core_data, query } = core_response;

    if (query && query != latestQuery) return;

    document.getElementById('my-accordion').innerHTML = ``;
    const categories = Object.keys(core_data);
    for (let category of categories) {
        if (focus_categories.length && !focus_categories.includes(category.toLowerCase())) continue;
        let resultsContent = `<div class="results-content">`
        let topList = `<div class="top-results">`;
        var i = 0;
        for (let reviewObj of Object.keys(core_data[category])) {
            let reviewData = core_data[category][reviewObj];
            topList += `<div data-url="${'/reviews/' + category.split(' ').join('-') + '/' + reviewData.id}" class="top-result ${i > 0 ? 'trl' : ''}">
                        <img class="tr-img" style="background-image: url('${reviewData.image_url}'); background-position: center; background-size: cover;"/>
                        <h1 class="tr-name">${reviewData.name}</h1>
                        <div class="tr-reviews">
                            <div class="rating-info">
                                <div class="rating-row">
                                    ${reviewData.overall_on_stars.map(star => `<img src="/static/img/star.png" class="star-item"/>`).join('')}
                                    ${reviewData.overall_off_stars.map(star => `<img src="/static/img/star.png" class="star-item gs"/>`).join('')}
                                </div>
                                    <h1 class="review-count">${reviewData.total_reviews} reviews</h1>
                                </div>
                        </div>
                    </div>`;
            i++;
            if (i > 3) break;
        }
        topList += `</div>`;
        resultsContent += topList;
        resultsContent += `<div style="width: 100%; height: 1px; background-color: rgba(0,0,0,0.05); opacity: 0; margin-top: 10px; margin-bottom: 10px;"></div>`;
        let objectsList = `<div class="list-results">`;
        for (let reviewObj of Object.keys(core_data[category])) {
            let reviewData = core_data[category][reviewObj];
            objectsList += ` <div data-url="${'/reviews/' + category.split(' ').join('-') + '/' + reviewData.id}" class="lr-container"> <h1 class="list-result lrm">${reviewData.name}</h1> <h1 class="list-result lr-info">${reviewData.total_score}/5, ${reviewData.total_reviews} reviews</h1>  </div>`;
        }
        objectsList += `</div`;
        resultsContent += objectsList;
        resultsContent += '</div>';
        document.getElementById('my-accordion').innerHTML += `
            <li>
                <div style="display: flex; flex-direction: row; align-items: center;">
                    <h1 class="ac-title">${category}</h1> <h3 class="rescount">${Object.keys(core_data[category]).length} results</h3>
                </div>
                <div>
                    ${resultsContent}
                </div>
            </li>`
    }


}

// Load picker items
let picker = document.querySelector('#pick-items');
for (const category of ALL_CATS) {
    picker.innerHTML += `<div class="category-container">  <div class="category-item">
        <h1 class="category-name">${category}</h1>
    </div> </div>`
}

// jQuery & SlickJS
$(document).ready(function () {
    $('.carousel').slick({
        slidesToShow: 5,
        arrows: true,
        autoplay: true,
        dots: true,
        centerMode: true,
        autoplaySpeed: 20000,
        swipeToSlide: true,
        touchThreshold: 20,
    });

    function cUpdate() {
        $('.carousel').slick("slickSetOption", "slidesToShow", Math.min(Math.round(window.innerWidth / 250.5), 11), true);
    }
    cUpdate();
    $(window).resize(function () {
        cUpdate();
    });

});

$('.category-item').click(function (event) {
    let focusCategory = event.currentTarget.innerText.trim();
    let r = $(event.currentTarget).toggleClass('category-focus');
    let enabled = r[0].className.includes('category-focus');
    if (enabled) {
        focus_categories.push(focusCategory.toLowerCase());
    } else {
        focus_categories = focus_categories.filter(i => i !== focusCategory.toLowerCase());
    }
    updatePage(latestQuery);
});



function updatePage(query) {
    if (query != latestQuery) return;
    fetch(`/core-data-query${query ? '?query=' + query : ''}`).then(resp => resp.json()).then(updateView).then(() => {
        $("#my-accordion").accordionjs({
            closeAble: true,
            activeIndex: [1, 2, 3],
        });

        $('.lr-container').click((event) => {
            window.location = event.currentTarget.getAttribute('data-url');
        })

        $('.top-result').click((event) => {
            window.location = event.currentTarget.getAttribute('data-url');
        })

    })
}

jQuery(document).ready(function ($) {
    updatePage();
});

$('.lr-container').click((event) => {
    window.location = event.currentTarget.getAttribute('data-url');
})

$('.top-result').click((event) => {
    window.location = event.currentTarget.getAttribute('data-url');
})

let latestType = null;
let oldData = {};
function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const autoCompleteJS = new autoComplete({
    placeHolder: "Search for professors, residence halls, clubs...",
    data: {
        src: async (query) => {
            latestType = query;

            await timeout(200);
            if (latestType != query) return oldData;
            const source = await fetch(`/search-opt?query=${query}`);
            const data = await source.json();
            oldData = data;
            return data;
        },
        cache: false,
        keys: ["name"]
    },
    resultItem: {
        highlight: true
    },
    searchEngine: 'loose',
    query: (input) => {
        latestQuery = input;
        setTimeout(() => {
            updatePage(input);
        }, 200);
        return input;
    },
    events: {
        input: {
            selection: (event) => {
                const selection = event.detail.selection;
                const name = selection.value[selection.key];
                autoCompleteJS.input.value = name;

                window.location.href = `/reviews/${selection.value['category']}/${selection.value['id']}`;
            }
        },


    }
});
