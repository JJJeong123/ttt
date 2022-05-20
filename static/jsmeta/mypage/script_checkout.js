async function cancelOrder(order_id){
  if (!confirm('주문을 취소하시겠습니까?')) {
    return;
  }
  const url = '/mypage/order-history';

  const response = await fetch(url, {
    method: 'DELETE',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    body: JSON.stringify({
      order_id: order_id,
    })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  if(result.success){
    alert('취소되었습니다');
    $("#order-table").load(location.href + " #order-table");
  }
  else{

  }
}

//장바구니에서 가져온 상품을 출력
function displayProducts(products){
  let parent=document.getElementsByClassName("checkout__products")[0];
  let total_price=0;

  products.forEach(element => {
    total_price += parseInt(element.price);
    let [figure, div, b, img, figcaption, span, div_total]
      = [
        document.createElement('figure'),
        document.createElement('div'),
        document.createElement('b'),
        document.createElement('img'),
        document.createElement('figcaption'),
        document.createElement('span'),
        document.createElement('div')
      ];
   
    figure.setAttribute('class', 'itemside align-items-center mb-4');
    div.setAttribute('class', 'aside');
    b.setAttribute('class', 'badge bg-secondary rounded-pill');
    b.innerText=element.amount;
    img.setAttribute('src', element.img);
    img.setAttribute('class', 'img-sm rounded');
    img.setAttribute('onclick', "window.open('/product/product-detail/"+element.id +"','_self');");
    img.setAttribute('style', 'cursor:pointer;')
    figcaption.setAttribute('class', 'info');
    span.setAttribute('onclick', "window.open('/product/product-detail/"+element.id +"','_self');");
    span.setAttribute('style', 'cursor:pointer;')
    span.innerText=element.name;
    div_total.setAttribute('class', 'price text-muted');
    div_total.innerText=parseInt(element.price).toLocaleString()+'원';

    div.append(b);
    div.append(img);
    figure.append(div);

    figcaption.append(span);
    figcaption.append(div_total);
    figure.append(figcaption);

    parent.append(figure);
  });

  document.getElementsByClassName('checkout__total')[0].innerText=total_price.toLocaleString()+'원';
}

document.addEventListener("DOMContentLoaded", function(){

  //장바구니에서 선택한 상품을 가져옴
  const products=JSON.parse(window.localStorage.getItem("products"));
  displayProducts(products);

  //for nav-tab
  document.querySelectorAll('.box-check').forEach(function(element) {
    element.addEventListener('click', function(event){

      document.querySelectorAll('.box-check').forEach(function(element){
        element.classList.remove('active');
      })
      
      element.classList.add('active');
    });
  });
});

//배송지 목록을 모달로 가져옴
async function openModal(){
  const url = '/mypage/checkout-address';
  const response = await fetch(url, {
      method: 'GET',
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  if(result.success === true) {

    let table=document.getElementById('address-table');
    removeAllChildren(table);
    let addresses=result.addresses;

    addresses.forEach(function(element){

      let div=document.createElement('div');
      let article=document.createElement('article');
      let b=document.createElement('b');
      let i=document.createElement('i');
      let span=document.createElement('span');

      div.setAttribute("class", "col-md-12");
      article.setAttribute("class", "box col-md-12");
      b.setAttribute("class", "mx-2 text-muted");
      i.setAttribute("class", "fa fa-map-marker-alt");
      span.setAttribute("class", "col-md-9");
      span.setAttribute("style", "cursor: pointer;");
      span.setAttribute("onclick", "showAddress(this);");
      span.setAttribute("id", element.id);
      span.setAttribute("data-name", element.name);
      span.setAttribute("data-call", element.call);
      span.setAttribute("data-code", element.code);
      span.innerText=element.ad_detail;

      b.append(i);
      article.append(b, span);
      div.append(article);

      table.append(div);
    })
    $('#modal__address').modal('show');
  }
}

function closeModal(){
  $('#modal__address').modal('hide');
}

function showAddress(element){

  let parent=document.getElementById("address__selected");

  if(parent.hasChildNodes()){
    document.getElementsByClassName("address__detail")[0].value=element.innerText;
    document.getElementsByClassName("address__code")[0].value=element.getAttribute("data-code");
    document.getElementsByClassName("address__name")[0].value=element.getAttribute("data-name");
    document.getElementsByClassName("address__call")[0].value=element.getAttribute("data-call");

    $('#modal__address').modal('hide');
    
    return;
  }

  let div=document.createElement('div');
  let label=document.createElement('label');
  let input=document.createElement('input');
  
  div.setAttribute("class", "col-sm-8 mb-3");
  label.innerText="주소";
  input.setAttribute("type", "text");
  input.setAttribute("class", "form-control address__detail");
  input.setAttribute("readonly", true);
  input.value=element.innerText;

  div.append(label, input);
  parent.append(div);

  div=document.createElement('div');
  label=document.createElement('label');
  input=document.createElement('input');

  div.setAttribute("class", "col-sm-4 col-6 mb-3");
  label.innerText="우편번호";
  input.setAttribute("type", "text");
  input.setAttribute("class", "form-control address__code");
  input.setAttribute("readonly", true);
  input.value=element.getAttribute("data-code");

  div.append(label, input);
  parent.append(div);

  div=document.createElement('div');
  label=document.createElement('label');
  input=document.createElement('input');

  div.setAttribute("class", "col-sm-6 mb-3");
  label.innerText="받으실 분";
  input.setAttribute("type", "text");
  input.setAttribute("class", "form-control address__name");
  input.setAttribute("readonly", true);
  input.value=element.getAttribute("data-name");

  div.append(label, input);
  parent.append(div);

  div=document.createElement('div');
  label=document.createElement('label');
  input=document.createElement('input');

  div.setAttribute("class", "col-sm-6 col-6 mb-3");
  label.innerText="연락처";
  input.setAttribute("type", "text");
  input.setAttribute("class", "form-control address__call");
  input.setAttribute("readonly", true);
  input.value=element.getAttribute("data-call");

  div.append(label, input);
  parent.append(div);
  parent.setAttribute("data-id", element.getAttribute("id"));

  $('#modal__address').modal('hide');

}

//Remove all children of the element
function removeAllChildren(e){
   let child = e.lastElementChild; 
   while (child) {
       e.removeChild(child);
       child = e.lastElementChild;
   }
}

function isValidInfo(order_type){
  // if(order_type === "2" || order_type === "3") {
  //   return true;
  // }
  if( (order_type==="0" || order_type==="1") &&
      (document.getElementsByClassName("address__detail")[0] === undefined ||
      document.getElementsByClassName("address__name")[0] === undefined ||
      document.getElementsByClassName("address__code")[0] === undefined ||
      document.getElementsByClassName("address__call")[0] === undefined))
    {
      alert("배송지 정보를 모두 입력해주세요");
      return false;
    }
  else if ( (order_type==="2" || order_type==="3") &&
    (document.getElementsByClassName("address__name")[0] === undefined ||
    document.getElementsByClassName("address__call")[0] === undefined))
    {
      alert("수령인 정보를 모두 입력해주세요");
      return false;
    } 
  
    return true;
}

async function checkout(){
  let order_type ="-1";

  document.querySelectorAll('.box-check').forEach(function(element){
    if(element.classList.contains("active")){
      order_type=element.getAttribute("value");
    }
  });
  if(!isValidInfo(order_type)){
    return;
  }
  const products=JSON.parse(window.localStorage.getItem("products"));

  const url = '/mypage/checkout';
  const response = await fetch(url, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        type: order_type,
        address: document.getElementById("address__selected").getAttribute("data-id"),
        name: document.getElementsByClassName("address__name")[0].value,
        call: document.getElementsByClassName("address__call")[0].value,
        products: products,
      })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();
  
  //성공 시 결과를 담아 checkout-confirm으로 로드
  if(result.success){
    localStorage.setItem("order", JSON.stringify(result.order));
    window.open('/mypage/checkout-confirm', '_self');
  }
  else{
    alert('문의가 등록되지 않았습니다. 다시 작성해주시기 바랍니다.');
  }
}