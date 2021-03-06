async function deleteFromCart(elem) {

    if (!confirm('삭제하시겠습니까?')) {
      return;
    }
    const cart_id = elem.getAttribute('id');

    const url = '/mypage/cart?cart_id=' + encodeURIComponent(cart_id);
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
        $("#cart-table").load(location.href + " #cart-table");
    }
};

//Update the number of items in cart in database
async function updateAmount(elem, product_id) {
  const amount = elem.value;

  const url = '/mypage/cart';
  const response = await fetch(url, {
      method: 'PUT',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        product_id: product_id,
        amount: amount,
    })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  if(result.success){
    updatePrice(product_id, amount);
  }

}

//Update price with new amount
async function updatePrice(product_id, amount){

  let price = document.getElementById('price-'+product_id);
  let new_price = parseInt(price.getAttribute('price'))*amount;

  price.innerText = new_price.toLocaleString() + '원';
  price.setAttribute('value', new_price);

  let total_price=0;

  let elements = document.getElementsByClassName("price");
  [].map.call(elements, function(elem) {
    total_price+=parseInt(elem.getAttribute('value'));
  });

  document.getElementById('total').innerText=total_price.toLocaleString();
  document.getElementById('total_price').innerText=total_price.toLocaleString();
}

function getAllIndexes(arr, val) {
  var indexes = [], i = -1;
  while ((i = arr.indexOf(val, i+1)) != -1){
      indexes.push(i);
  }
  return indexes;
}

//save products
function saveProducts(products){
  localStorage.setItem("products", JSON.stringify(products));
}

function passProducts(){
  let indexes=[];
  let products=[];

  //get indexes of checked inputs
  document.querySelectorAll('.product__checkbox').forEach(function (c, i, a) {
    if(c.checked){
      indexes.push(i);
    }
  });
  
  //get info of checked products using indexes
  document.querySelectorAll('.product__amount').forEach(function(c, i, a){
    if(indexes.includes(i)){
      let product={};

      product['amount'] = c.getAttribute('value');
      product['img'] = c.getAttribute('data-image');
      product['price'] = c.getAttribute('data-price');
      product['id'] = c.getAttribute('data-id');
      product['name'] = c.getAttribute('data-name');

      products.push(product);
    }
  });

  saveProducts(products);

}
