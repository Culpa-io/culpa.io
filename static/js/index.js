
    // Typing animation 
    var options = {
        strings: categories.map(i=>`Explore ${i}...`),
        typeSpeed: 80,
        backSpeed: 40,
        backDelay: 3000,
        loop: true,
        showCursor: true,
        };
    
    var typed = new Typed('#explore', options);
    document.querySelector('#explore').focus();

    // Load picker items
    let picker = document.querySelector('#pick-items');
    for (const category of categories){
        picker.innerHTML += `<div class="category-container">  <div class="category-item">
            <h1 class="category-name">${category}</h1>
        </div> </div>`
    }

    // jQuery & SlickJS
    $(document).ready(function(){
        $('.carousel').slick({
            slidesToShow: 5,
            swipeToSlide: true,
            arrows: false,
            autoplay: true,
            dots: true,
            centerMode: true,
            touchThreshold: 20,
            autoplaySpeed: 20000
        });
        $('.carousel').slick('slickGoTo', 2);
        $('.slick-slide').click( (event) => {
           let idx = parseInt(event.currentTarget.getAttribute('data-slick-index'));
           $('.carousel').slick('slickGoTo', idx);
        })


        function cUpdate() {
            $('.carousel').slick("slickSetOption", "slidesToShow", Math.min(Math.round(window.innerWidth/250.5), 11), true);
        }  
        cUpdate();
        $(window).resize(function(){
            cUpdate();
        });
    });

    $('.carousel').on('afterChange', function(event, slick, currentSlide, nextSlide){
        var cslide = $(slick.$slides.get(currentSlide)).text().trim().split(' ').join('-');
        $('.cmx').css({display: "none"});
        $(`.${cslide}`).css({display: "inline-block", width: "100%"});
    });


    $('.libraries').css({display: "inline-block", width: "100%"});

    $('#explore, #explore-button').click(() => {
        window.location = '/search';
    })

    $('#write-review').click(() => {
        window.location = '/compose';
    })

    $('.contribute-text').click(() => {
        window.location = '/compose';
    })

    $('.location-item').click((event) => {
        window.location = event.currentTarget.getAttribute('data-url');
    })
