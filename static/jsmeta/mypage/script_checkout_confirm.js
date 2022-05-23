document.addEventListener("DOMContentLoaded", function(){
  displayOrderInfo();
  
  //clear localstorage
  window.localStorage.removeItem('products');
  window.localStorage.removeItem('orders');
  window.localStorage.removeItem('discount_amount');

});

function displayOrderInfo(){

  const products=JSON.parse(window.localStorage.getItem("products"));
  const order=JSON.parse(window.localStorage.getItem("order"));
  const discount_amount=JSON.parse(window.localStorage.getItem("discount_amount"));

  let order_type="", total_price=0;

  if(order.type==='0') order_type="택배배송";
  else if(order.type==='1') order_type="근거리배송";
  else if(order.type==='2') order_type="드라이브스루";
  else if(order.type==='3') order_type="포장";
  
  products.forEach(element => {
    total_price += parseInt(element.price);
  });

  document.getElementsByClassName("order__no")[0].innerText="주문번호: "+order.no;
  document.getElementsByClassName("order__type")[0].textContent=order_type;
  document.getElementsByClassName("product__price")[0].innerText="상품금액: "+total_price.toLocaleString()+"원";
  document.getElementsByClassName("order__name")[0].innerText=order.name;
  document.getElementsByClassName("order__call")[0].innerText=order.call.slice(0, 3)+"-"+order.call.slice(3, 7)+"-"+order.call.slice(7, 11);
  document.getElementsByClassName("order__discount")[0].innerText="할인금액: "+discount_amount.toLocaleString()+"원";
  document.getElementsByClassName("order__price")[0].innerText="결제금액: "+(total_price-discount_amount).toLocaleString()+"원";
  
  if(order.address!=null){
    document.getElementsByClassName("order__address")[0].innerText=order.address;
  }

  displayProducts();
}

function displayProducts(){
  const products=JSON.parse(window.localStorage.getItem("products"));
  let parent=document.getElementsByClassName("products")[0];

  products.forEach(element => {
    let li=document.createElement('li');
    let figure=document.createElement('figure');
    let div=document.createElement('div');
    let img=document.createElement('img');
    let figcaption=document.createElement('figcaption');
    let p=document.createElement('p');
    let p_amount=document.createElement('p');
    let strong=document.createElement('strong');

    li.setAttribute("class", "col-xl-4 col-lg-6");
    figure.setAttribute("class", "itemside mb-3");
    div.setAttribute("class", "aside");
    img.setAttribute("width", "72");
    img.setAttribute("height", "72");
    img.setAttribute("src", element.img);
    img.setAttribute("class", "img-sm rounded border");
    figcaption.setAttribute("class", "info");
    p.setAttribute("class", "title");
    p.innerText=element.name;
    p_amount=element.amount+"개";
    strong.innerText=parseInt(element.price).toLocaleString()+"원";

    div.append(img);
    figcaption.append(p, p_amount, document.createElement("br"), strong);
    figure.append(div, figcaption);
    li.append(figure);
    parent.append(li);
  })
}