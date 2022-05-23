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

function openModal(element){
  let product_id=element.getAttribute("data-id");
  let product_name=element.getAttribute("data-name");
  let product_src=element.parentNode.parentNode.parentNode.children[0].children[0].children[0].children[0].getAttribute("src")

  document.getElementsByClassName("product__img")[0].setAttribute("value", product_id);
  document.getElementsByClassName("product__img")[0].setAttribute("src", product_src);
  document.getElementsByClassName("product__title")[0].innerText=product_name;

  $("#product-add").modal("show");
}

function closeModal(){
  $("#product-add").modal("hide");
}

async function addCart(){
  if(document.getElementsByClassName('product__amount')[0].value.length === 0) {
    alert('수량을 입력해주세요');
    return;
  }
  const product_id = document.getElementById('product__img').getAttribute('value');

  const url = '/product/product-detail/'+ product_id;
  const response = await fetch(url, {
    method: 'POST',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    body: JSON.stringify({
      amount: document.getElementsByClassName('product__amount')[0].value,
    })
  })
  .catch((error)=>{
      alert(error);
  })

  const result = await response.json();
  
  if(result.success){
    alert('상품을 장바구니에 담았습니다.');
    closeModal();
  }
};
