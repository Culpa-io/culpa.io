const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var canProceed = false;
var CUR_ID;
var CUR_NAME;
var CUR_CAT;


var canProceedSubmit = false;
var CUR_ID_SUBMIT;
var CUT_NAME_SUBMIT;


$(document).ready(function () {
    $('select').niceSelect();
});

$('.cont').click(function () {
    if (canProceed) {

    } else {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'You need to select something from the search bar to review first!'
        });
    }
});

function newSelect(evt, category) {
    if ($('select').val() === 'other') {
        $('#search-submit').css({ height: 50, opacity: 1 });
    } else {
        $('#search-submit').css({ height: 0, opacity: 0 });
    }

    try {
        window.acJS?.unInit();
    } catch (e) { };
    window.acJS = createAutocomplete('#search-submit', `Search for ${category}...`, `${category}`);
}

function updateDisplay(data) {
    const propImage = document.getElementById('pi');
    const propName = document.getElementById('pn');
    const propCount = document.getElementById('pc');
    $('#search-submit').val('');

    if (data) {
        CUR_CAT = data.category_name;
        propImage.style.backgroundImage = `url('${data.image_url}')`;
        $('.abtr').css({ display: 'block' })
        propName.innerHTML = data.name;
        propCount.innerHTML = `${data.num_reviews} reviews`;
        $('.review-pending').removeClass('rpb');
        $('#revnotice').html(`You're about to review a ${CUR_CAT}...`);
        $('.write-review').css({ opacity: 1 });

        let OTHER = `<option value="other">Other</option>`;

        if (!!data.professors.length) {
            $('.nice-select').css({ display: 'inline-block' });
            document.querySelector('#prof-select').innerHTML = data.professors.map(p => `<option value="${p.uni}">${p.name} (${p.uni})</option>`).join(`\n`) + OTHER;
            $('select').niceSelect();
            $('select').change((evt) => newSelect(evt, 'professors'));
            $('select').niceSelect('update');
        } else if (!!data.courses.length) {
            $('.nice-select').css({ display: 'inline-block' });
            document.querySelector('#prof-select').innerHTML = data.courses.map(c => `<option value="${c.roid}">${c.name}</option>`).join(`\n`) + OTHER;
            $('select').niceSelect();
            $('select').change((evt) => newSelect(evt, 'courses'));
            $('select').niceSelect('update');
        } else {
            $('.nice-select').css({ display: 'none' });
            $('#search-submit').css({ height: 0, opacity: 0 });
            window.acJS?.unInit();
        }

    } else {
        $('#search-submit').css({ height: 0, opacity: 0 });
        propImage.style.backgroundImage = `url('/static/img/user.png')`;
        propName.innerHTML = `Professor Example`;
        propCount.innerHTML = `294 reviews`;
        $('.review-pending').addClass('rpb');
        $('#revnotice').html(`You're about to review...`);
        $('.write-review').css({ opacity: 0 });
        $('.abtr').css({ display: 'none' })
        window.acJS?.unInit();
    }
}


const autoCompleteJS = new autoComplete({
    placeHolder: "Search for professors, residence halls, clubs...",
    data: {
        src: async (query) => {
            const source = await fetch(`/search-opt?query=${query}`);
            const data = await source.json();


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
        if (input === ``) {
            updateDisplay();
            canProceed = false;
        }

        return input;
    },
    events: {
        input: {
            selection: (event) => {
                const selection = event.detail.selection;
                const name = selection.value[selection.key];
                autoCompleteJS.input.value = name;

                CUR_ID = selection.value.id;
                CUR_NAME = name;


                fetch(`/getrodata?id=${selection.value.id}`).then(res => res.json()).then(json => {
                    updateDisplay(json);
                    canProceed = true;
                })
            }
        },


    }
});

function createAutocomplete(selector, placeholder, category) {

    return new autoComplete({
        placeHolder: placeholder,
        data: {
            src: async (query) => {
                const source = await fetch(`/search-opt?query=${query}&filterby=${category}`);
                const data = await source.json();


                return data;
            },
            cache: false,
            keys: ["name"]
        },
        selector: selector,
        resultItem: {
            highlight: true
        },
        searchEngine: 'loose',
        query: (input) => {

            if (input === ``) {
                canProceedSubmit = false;
            }

            return input;
        },
        events: {
            input: {
                selection: (event) => {
                    const selection = event.detail.selection;
                    const name = selection.value[selection.key];

                    $(selector).val(name);

                    CUR_ID_SUBMIT = selection.value.id;
                    CUR_NAME_SUBMIT = name;

                    canProceedSubmit = true;

                    // fetch(`/getrodata?id=${selection.value.id}`).then(res => res.json()).then(json => {
                    //     // updateDisplay(json);
                    //     console.log(json);
                    //     // canProceed = true;
                    // })
                }
            },


        }
    });

}


const e_target = new URL(window.location.href).searchParams.get('target');
if (e_target) {
    CUR_ID = e_target;
    CUR_NAME = new URL(window.location.href).searchParams.get('name');
    fetch(`/getrodata?id=${e_target}`).then(res => res.json()).then(json => {
        updateDisplay(json);
        canProceed = true;
    });
} else {
    updateDisplay();
}

var starState = null;
var cIdxGlobal = null;
$('.star-item').hover((event) => {
    let cStar = event.currentTarget;
    let cIdx = parseInt(cStar.id.replace('s', ''));
    for (var i = 1; i <= cIdx; i++) {
        let star = document.getElementById(`s${i}`);
        $(star).removeClass('gs');
    }

    for (var i = cIdx + 1; i <= 5; i++) {
        let star = document.getElementById(`s${i}`);
        $(star).addClass('gs');
    }

    cIdxGlobal = cIdx;
});

$('.star-item').click(function () {
    starState = cIdxGlobal;
})

$('.rating-row').mouseleave(function () {
    for (var i = 1; i <= starState; i++) {
        let star = document.getElementById(`s${i}`);
        $(star).removeClass('gs');
    }
    for (var i = starState + 1; i <= 5; i++) {
        let star = document.getElementById(`s${i}`);
        $(star).addClass('gs');
    }
})


$('.submit-review').click(function () {
    // Check invalid 

    const title = document.getElementById('title-submit').value;
    const thoughts = document.getElementById('thoughts-submit').value;
    let selectMeta = document.querySelector('#prof-select').value;

    if (selectMeta === 'other' && canProceedSubmit) {
        selectMeta = CUR_ID_SUBMIT?.toString();
    }

    if (starState === null || !thoughts || !title || !CUR_ID || (selectMeta === 'other' && !canProceedSubmit)) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'You need to provide a rating, title, and review before submitting!'
        });
        return;
    }

    const data = {
        title: title,
        review: thoughts,
        rating: starState,
        target_id: CUR_ID,
        category: CUR_CAT,
        metadata: selectMeta || undefined,
    };

    fetch(`/submitreview`, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
    }).then(response => response.json()).then(json => {
        if (json.success) {
            Swal.fire({
                icon: 'success',
                title: `${CUR_NAME} Review Submitted!`,
                text: 'Thanks for submitting a review. Reviews are generally approved within 1-2 days, so check back soon!'
            }).then(result => {
                window.location = '/';
            })
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong! Please try again later.'
            });
        }
    })
})
