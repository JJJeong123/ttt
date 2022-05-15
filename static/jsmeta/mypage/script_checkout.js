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