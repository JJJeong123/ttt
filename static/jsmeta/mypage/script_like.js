async function likeProduct(element, product_id){
    const isLiked = element.firstElementChild.classList.contains("heart-primary");

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
    });

    if (isLiked){
      element.firstElementChild.classList.remove("heart-primary");
      element.firstElementChild.classList.add("heart-white");
    }
    else {
      element.firstElementChild.classList.remove("heart-white");
      element.firstElementChild.classList.add("heart-primary");
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

