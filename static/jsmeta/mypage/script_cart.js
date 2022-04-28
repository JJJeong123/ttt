async function deleteFromCart(elem) {

    if (!confirm('삭제하시겠습니까?')) {
      return;
    }
    const cart_id = elem.getAttribute('id');

    const url = '/mypage/cart?cart_id=' + encodeURIComponent(cart_id);
    const response = await fetch(url, {
        method: 'PUT',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify({
          product_id: elem.getAttribute('value'),
      })
    })
    .catch((error) => {
        alert(error);
    });
  
    const result = await response.json();
  
    if(result.success === true) {
        $("#cart-table").load(location.href + " #cart-table");
    }
};
  
