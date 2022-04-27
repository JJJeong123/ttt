document.getElementById('product__cart').addEventListener('click', async (event)=>{

  if(document.getElementById('product__amount').value.length === 0) {
    alert('수량을 입력해주세요');
    return;
  }
  const product_id = document.getElementById('product__img').getAttribute('value');

  const url = '/product/product-detail/'+ product_id;
  const response = await fetch(url, {
    method: 'POST',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    body: JSON.stringify({
      amount: document.getElementById('product__amount').value,
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
