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

  const url = '/mypage/address';
  const response = await fetch(url, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        code: document.getElementById('address').getAttribute('value'),
        ad_detail: document.getElementById('address').getAttribute('name')
                      +' '+ document.getElementById('address-detail').value,
        call: document.getElementById('address-call').value,
        name: document.getElementById('address-member').value,
              
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
/* 배송지 수정 및 삭제 모달 열기 */
async function openModal(elem){

  const url = '/mypage/address-modal?id=' + encodeURIComponent(elem.getAttribute('value'));
  const response = await fetch(url, {
      method: 'GET',
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  // 모달을 닫고 리로드
  if(result.success === true) {
    $('#address-edit').modal('show');

    document.getElementById('addressToEdit').value=result.address['ad_detail'];
    document.getElementById('addressToEdit').setAttribute('value', result.address['id']);
    document.getElementById('address-name').value=result.address['ad_name'];
    document.getElementById('address-call').value=result.address['call'];
    document.getElementById('address-member').value=result.address['name'];
  }
}

/* 배송지 수정 */
async function editAddress(){

  const url = '/mypage/address';
  const response = await fetch(url, {
      method: 'PUT',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        id: document.getElementById('addressToEdit').getAttribute('value'),
        ad_name: document.getElementById('address-name').value,
        call: document.getElementById('address-call').value,
        name: document.getElementById('address-member').value,
    })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  // 모달을 닫고 리로드
  if(result.success === true) {
    $('#address-edit').modal('hide');
    $("#address-table").load(location.href + " #address-table");

    alert('수정되었습니다.');
  }
}

/* 배송지 삭제 */
async function deleteAddress(){

  const url = '/mypage/address';
  const response = await fetch(url, {
      method: 'DELETE',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        id: document.getElementById('addressToEdit').getAttribute('value'),
    })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  // 모달을 닫고 리로드
  if(result.success === true) {
    $('#address-edit').modal('hide');
    $("#address-table").load(location.href + " #address-table");
    
    alert('삭제되었습니다.');
  }
}


function closeModalToAdd(){
  $('#address-add').modal('hide');
}
function closeModalToEdit(){
  $('#address-edit').modal('hide');
}