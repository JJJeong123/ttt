document.getElementById('product__cart').addEventListener('click', async (event)=>{

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
    alert('상품을 장바구니에 담았습니다.')
  }
});

function updateAmount(element, price){
  let total_price=document.getElementsByClassName("total-price")[0];
  console.log()
  let num=element.value;

  total_price.innerText=(price*num).toLocaleString()+"원";
}