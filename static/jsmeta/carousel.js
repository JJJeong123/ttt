function scrollL() {
  let x = document.getElementsByClassName("items")[0];
  let step = window.outerWidth / 2;
  x.scrollLeft -= step;
}

function scrollR() {
  let x = document.getElementsByClassName("items")[0];
  let step = window.outerWidth / 2;
  x.scrollLeft += step;
}

function getScrollVal() {
  setTimeout(() => {
    let x = document.getElementsByClassName("items")[0];
    let el = document.getElementsByClassName("left_arrow")[0];
    if (x.scrollLeft == 0) {
      el.style.display = "none";
    } else {
      el.style.display = "flex";
    }
    let el2 = document.getElementsByClassName("right_arrow")[0];
    let right = x.scrollWidth - (x.scrollLeft + x.clientWidth) + 1;
    if (right <= 2) {
      el2.style.display = "none";
    } else {
      el2.style.display = "flex";
    }
  }, 550);
}

getScrollVal();


// const swiper = new Swiper(".swiper-container", {
//   slidesPerView: 2,
//   slidesPerGroup: 1,
//   centeredSlides: true,
//   loop: true,
//   navigation: {
//         nextEl: '.swiper-button-next',
//         prevEl: '.swiper-button-prev',
//       },
//    breakpoints: {
//     // when window width is >= 600px
//     600: {
//       slidesPerView: 3,
//       slidesPerGroup: 3,
//       spaceBetween: 5,
//       centeredSlides: true
      
//     },
//      // when window width is >= 900px
//      900: {
//       slidesPerView: 3,
//       slidesPerGroup: 3,
//       spaceBetween: 5,
//        centeredSlides: false
      
//     },
//     // when window width is >= 1200px
//     1200: {
//       slidesPerView: 4,
//       slidesPerGroup: 4,
//       spaceBetween: 5,
//       centeredSlides: false
//     },
     
//      // when window width is >= 1500px
//      1500: {
//        slidesPerView: 5,
//        slidesPerGroup: 5,
//        spaceBetween: 5,
//        centeredSlides: false
//      },
     
//      // when window width is >= 1800px
//     1800: {
//       slidesPerView: 5,
//       slidesPerGroup: 5,
//       spaceBetween: 5,
//       centeredSlides: false
//     }
//   }
// });
