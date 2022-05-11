async function deleteQuestion(qna_id){
  const url = '/mypage/product_qna-list';
  
  const response = await fetch(url, {
    method: 'DELETE',
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    body: JSON.stringify({
      qna_id: qna_id
    })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();
  
  if(result.success){
    alert('삭제되었습니다.');
    window.open('/mypage/product_qna-list', '_self');
  }
  else{
    alert('삭제되지 않았습니다. 다시 시도해주시기 바랍니다.');
    window.open('/mypage/product_qna-list', '_self');
  }
}