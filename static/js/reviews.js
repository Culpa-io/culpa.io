
let picker = document.querySelector('#pick-items');
var i = 0;
for (const reviewData of sros) {
    picker.innerHTML += `<div data-url="${'/reviews/' + META_CAT.split(' ').join('-') + '/' + reviewData.id}" class="top-result t${i}">
                            <img class="tr-img" style="background-image: url('${reviewData.image_url}'); background-position: center; background-size: cover;"/>
                            <h1 class="tr-name">${reviewData.name}</h1>
                            <div class="tr-reviews">
                                <div class="sa-rating-info">
                                    <div class="sa-rating-row">
                                        ${reviewData.overall_on_stars.map(star => `<img src="/static/img/star.png"class="star-item"/>`).join('')}
                                        ${reviewData.overall_off_stars.map(star => `<img src="/static/img/star.png"class="star-item gs"/>`).join('')}
                                    </div>
                                        <h1 class="sa-review-count">${reviewData.total_reviews} reviews</h1>
                                    </div>
                            </div>
                        </div>`;
    i++;
}



function cUpdate() {
    var divconst;
    if (HAS_META) {
        divconst = 355.5;
    } else {
        divconst = 225.5;
    }
    $('.carousel').slick("slickSetOption", "slidesToShow", Math.min(Math.round(window.innerWidth / divconst), sros.length), true);
}


if (HAS_META) {
    $('.top-result')
        .mousedown(function (event) {
            $(window).mousemove(function () {
                isDragging = true;
                $(window).unbind("mousemove");
            });
        })
        .mouseup(function (event) {
            var wasDragging = isDragging;
            isDragging = false;
            $(window).unbind("mousemove");
            if (!wasDragging) {
                window.location = event.currentTarget.getAttribute('data-url');
            }
        });
} else {
    $('.top-result').click(function () {
        window.location = event.currentTarget.getAttribute('data-url');
    })
}


$(document).ready(function () {
    $('select').niceSelect();


    $('.carousel').slick({
        slidesToShow: 4,
        arrows: true,
        autoplay: true,
        dots: true,
        centerMode: !HAS_META,
        autoplaySpeed: 20000,
        swipeToSlide: true,
        touchThreshold: 20,
    });

    cUpdate();
    $(window).resize(function () {
        cUpdate();
    });


});




$('.new-review, .war').click(function () {
    window.location = `/compose?target=${META_ID}&name=${META_NAME}`;
})

words = words.filter(x => x.length < 40);
let qWords = words.map(w => `“${w}”`);
let qWordsUnique = [...new Set(qWords)];
qWordsUnique = qWordsUnique.sort((a, b) => { qWords.filter(i => i === a).length - qWords.filter(i => i === b).length }).splice(0, 10);
if (qWordsUnique.length <= 2) {
    document.querySelector('.word-cloud').style.display = 'none';
    document.querySelector('#sepinr').style.opacity = 0;
    document.querySelector('#sepinr').style.marginBottom = -70;
}
var layout = d3.layout.cloud()
    .size([window.innerWidth, 320])
    .words(qWordsUnique.map(function (d) {
        return { text: d, size: 15 + Math.random() * 45 };
    }))
    .padding(20)
    .rotate(function () { return Math.random() * 40 - 20; })
    .font("Courgette")
    .fontSize(function (d) { return d.size; })
    .on("end", draw);

layout.start();

function draw(words) {
    d3.select(".word-cloud").append("svg")
        .attr("width", layout.size()[0])
        .attr("height", layout.size()[1])
        .append("g")
        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function (d) { return d.size + "px"; })
        .style("font-family", "Courgette")
        .attr("text-anchor", "middle")
        .style("fill", `rgb(76, 77, 220)`)
        .attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function (d) { return d.text; });
}



if (!HAS_META) {
    $('.course-name').css({ display: "none" });
}