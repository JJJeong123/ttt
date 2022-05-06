/* 배송지 검색 */
document.getElementById('address-button').addEventListener('click', ()=>{
  new daum.Postcode({
    oncomplete: function(data) {
      $('#address-add').modal('show');

      document.getElementById('address-detail').focus();

      document.getElementById('address').value=data.address;
      document.getElementById('address').setAttribute('name', data.address);
      document.getElementById('address').setAttribute('value', data.zonecode);
    }
  }).open();
});

/* 배송지 재검색 */
document.getElementById('address-relookup').addEventListener('click', ()=>{
  new daum.Postcode({
    oncomplete: function(data) {
        $('#address-add').modal('show');

        document.getElementById('address-detail').focus();

        document.getElementById('address').value=data.address;
        document.getElementById('address').setAttribute('name', data.address);
        document.getElementById('address').setAttribute('value', data.zonecode);
      },
    onclose: function(state) {
      document.getElementById('address-detail').value="";
    }
  }).open();
});

/* 배송지 추가 */
async function addAddress(){
  console.log(document.getElementById('address').getAttribute('name')
  + document.getElementById('address-detail').value);

  const url = '/mypage/address';
  const response = await fetch(url, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        code: document.getElementById('address').getAttribute('value'),
        ad_detail: document.getElementById('address').getAttribute('name')
                      +' '+ document.getElementById('address-detail').value,
    })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  // 모달을 닫고 리로드
  if(result.success === true) {
    document.getElementById('address-detail').value="";
    $('#address-add').modal('hide');
    $("#address-table").load(location.href + " #address-table");
  }

}

function openModal(){
  $('#address-edit').modal('show');

  //document.
}

function closeModalToAdd(){
  $('#address-add').modal('hide');
}
function closeModalToEdit(){
  $('#address-edit').modal('hide');
}