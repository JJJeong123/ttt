async function likeProduct(product_id){
    const isLiked = document.getElementsByClassName('heart-primary').length > 0;

    const url = '/mypage/like';
    const response = await fetch(url, {
      method: 'PUT',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        id: product_id,
        isLiked: isLiked,
      })
    })
    .catch((error) => {
        alert(error);
    })
    if (isLiked){
      document.getElementById("heart").classList.remove("heart-primary");
      document.getElementById("heart").classList.add("heart-white");

    }
    else {
      document.getElementById("heart").classList.remove("heart-white");
      document.getElementById("heart").classList.add("heart-primary");
    }
}

async function deleteFromWishlist(elem) {

  if (!confirm('삭제하시겠습니까?')) {
    return;
  }

  const url = '/mypage/like';
  const response = await fetch(url, {
      method: 'DELETE',
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
      $("#like-table").load(location.href + " #like-table");
  }
};

