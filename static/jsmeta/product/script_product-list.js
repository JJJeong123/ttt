document.addEventListener("DOMContentLoaded", function(){
  displayProducts();
});

async function displayProducts(){
  let category=window.location.href.split("/").pop();
  const url = `/product/product-grid?cat=${category}`;

  const response = await fetch(url, {
    method: 'GET',
  })
  .catch((error) => {
    alert(error);
  });

  const result = await response.json();
  
  //display products grid
  if (result.success && result.products.length>0) {

    $("#pagination").twbsPagination({
      totalPages: Math.ceil(result.products.length / 20), // from $.ajax response
      visiblePages: 5,
      first: "<<",
      last: ">>",
      prev: "이전",
      next: "다음",
      onPageClick: function (event, page) {
        setContent(page, result);
      },
    });
  } else {
    
  }

}

/* Set contents for pagination */
function setContent(page, result) {
  let list=document.getElementById("product__list");
  list.innerHTML="";

  const products=result.products;

  for (let i = 0; i < 20; i++) {
    let index = (page - 1) * 20 + i;
        
    if (products.length < index + 1) {
      break;
    }

    let [div_item, figure, div_img, span, a_heart, i_heart, img, figcaption, span_title, p, div_wrap, a_cart,
          i_cart, div_price, strong, del, small]
    = [
      document.createElement("div"),
      document.createElement("figure"),
      document.createElement("div"),
      document.createElement("span"),
      document.createElement("a"),
      document.createElement("i"),
      document.createElement("img"),
      document.createElement("figcaption"),
      document.createElement("span"),
      document.createElement("p"),
      document.createElement("div"),
      document.createElement("a"),
      document.createElement("i"),
      document.createElement("div"),
      document.createElement("strong"),
      document.createElement("del"),
      document.createElement("small"),
    ];

    div_item.setAttribute("class", "col-lg-3 col-sm-6 col-12 my-5");
    figure.setAttribute("class", "card card-product-grid");
    div_img.setAttribute("class", "img-wrap px-1 pt-1");
    //div_img.setAttribute("onclick", "window.open('/product/product-detail/"+products[index].id +"','_self')");
    div_img.setAttribute("style", "cursor:pointer; height: 355px; border-radius: 2px;");
    span.setAttribute("class", "topbar");
    a_heart.setAttribute("class", "btn btn-sm float-end a__heart");
    a_heart.setAttribute("onclick", `likeProduct(this, ${products[index].id})`);
    i_heart.setAttribute("class", "fa fa-heart");
    img.setAttribute("src", result.imgs[index]);
    figcaption.setAttribute("class", "info-wrap px-2 py-1");
    figcaption.setAttribute("onclick", "window.open('/product/product-detail/"+products[index].id +"','_self')");
    figcaption.setAttribute("style", "cursor:pointer");
    
    if(result.like[index]>0){
      i_heart.classList.add("heart-primary");
    }
    else{
      i_heart.classList.add("heart-white");
    }
    //span_title.setAttribute("class", "text-muted");
    p.setAttribute("class", "title pt-1");
    p.setAttribute("style", "height: 55px;")
    div_wrap.setAttribute("class", "bottom-wrap");
    a_cart.setAttribute("class", "btn btn-light btn-icon float-end");
    i_cart.setAttribute("class", "fa fa-shopping-cart");
    div_price.setAttribute("class", "price-wrap lh-sm");
    strong.setAttribute("class", "price");
    del.setAttribute("class", "price-old mx-2");
    strong.setAttribute("class", "price");
    small.setAttribute("class", "text-danger");

    p.innerText=products[index].name;
    strong.innerText=parseInt(products[index].price).toLocaleString()+'원';
    small.innerText="10% 할인";
    del.innerText=(parseInt(products[index].price)*1.1).toLocaleString()+'원';

    a_heart.append(i_heart);
    span.append(a_heart);
    div_img.append(span, img);
    figcaption.append(span_title, p);
    strong.append(del, document.createElement("br"));
    div_price.append(strong, small);
    a_cart.append(i_cart);
    div_wrap.append(a_cart, div_price);
    figure.append(div_img, figcaption, div_wrap);
    div_item.append(figure);

    list.append(div_item);
  }
}