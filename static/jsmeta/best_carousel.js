let erl = document.getElementsByClassName("left_arrow")
console.log(erl);
console.log(document.getElementsByClassName("items"))

function scrollL() {
    let x = document.getElementsByClassName("items")[0];
    let item = document.getElementsByClassName("item")[0];
    let step = item.offsetWidth * 4 + 4;
    x.scrollLeft -= step;
  }
  
  function scrollR() {
    let x = document.getElementsByClassName("items")[0];
    let item = document.getElementsByClassName("item")[0];
    let step = item.offsetWidth * 4 + 4;
    x.scrollLeft += step;
  }
  
  function getScrollVal() {
    setTimeout(() => {
      let p = document.getElementById("carousel");
      let style = p.currentStyle || window.getComputedStyle(p);
  
      let x = document.getElementsByClassName("items")[0];
      let el = document.getElementsByClassName("left_arrow")[0];
    
      if (x.scrollLeft == 0) {
        el.style.display = "none";
      } 
      else {
        el.style.display = "flex";
        el.style.left = parseInt(style.marginLeft) + x.scrollLeft + "px";
      }
  
      let el2 = document.getElementsByClassName("right_arrow")[0];
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
  
  function agetScrollVal() {
    setTimeout(() => {
      let p = document.getElementById("acarousel");
      let style = p.currentStyle || window.getComputedStyle(p);
  
      let x = document.getElementsByClassName("items")[1];
      let el = document.getElementsByClassName("left_arrow")[1];
    
      if (x.scrollLeft == 0) {
        el.style.display = "none";
      } 
      else {
        el.style.display = "flex";
        el.style.left = parseInt(style.marginLeft) + x.scrollLeft + "px";
      }
  
      let el2 = document.getElementsByClassName("right_arrow")[1];
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