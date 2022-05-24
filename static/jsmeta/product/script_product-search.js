function openModal(element){
  let parent=element.parentNode.parentNode;

  let src=parent.children[0].children[1].getAttribute("src");
  let product_id=parent.getAttribute("value");
  let product_title=parent.children[1].children[0].innerText;

  $("#product-add").modal("show");

  document.getElementsByClassName("product__img")[0].setAttribute("value", product_id);
  document.getElementsByClassName("product__img")[0].setAttribute("src", src);
  document.getElementsByClassName("product__title")[0].innerText=product_title;

}

function closeModal(){
  $("#product-add").modal("hide");
  document.getElementsByClassName("product__amount")[0].value=1;
}

async function addToCart(){

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
