function openModal(){
  $('#qna-add').modal('show');
}

function closeModal(){
  $('#qna-add').modal('hide');
}

async function saveQuestion(product_id){

  let title=document.getElementById('question-title').value;
  let content=document.getElementById('question-content').value;
  
  const url = '/product/qna-post';
  const response = await fetch(url, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        title: title,
        content: content,
        product_id: product_id,
      })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  if(result.success){
    alert('문의가 성공적으로 등록되었습니다.');
    closeModal();
  }
  else{
    alert('문의가 등록되지 않았습니다. 다시 작성해주시기 바랍니다.');
  }

}