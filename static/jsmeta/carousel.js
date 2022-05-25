function scrollL(element) {
  let x = element.parentNode;
  let item = element.parentNode.children[1];

  let step = item.offsetWidth * 4 + 4;
  x.scrollLeft -= step;
}

function scrollR(element) {
  let x = element.parentNode;
  let item = element.parentNode.children[1];

  let step = item.offsetWidth * 4 + 4;
  x.scrollLeft += step;
}

function getScrollVal(element) {
  setTimeout(() => {
    let p = element.parentNode;
    let style = p.currentStyle || window.getComputedStyle(p);

    let x = element;
    let el = element.firstElementChild;
  
    if (x.scrollLeft == 0) {
      el.style.display = "none";
    } 
    else {
      el.style.display = "flex";
      el.style.left = parseInt(style.marginLeft) + x.scrollLeft + "px";
    }

    let el2 = element.lastElementChild;
    let right = x.scrollWidth - (x.scrollLeft + x.clientWidth) + 1;
    
    el2.style.left="auto";

    if (right <= 2) {
      el2.style.display = "none";
      el.style.left = (x.scrollLeft - el2.clientWidth) + "px";
    } 
    else {
      el2.style.display = "flex";
      el2.style.left = (parseInt(style.marginLeft) + x.scrollLeft + x.clientWidth - el2.clientWidth) + "px";
    }
  }, 550);
}