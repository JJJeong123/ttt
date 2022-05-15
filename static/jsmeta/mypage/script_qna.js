function addImage(e){
  e = e || window.event;
  let target = e.target || e.srcElement;

  if(document.getElementById('qna-img-preview')){
    document.getElementById('qna-img-preview').setAttribute('src', URL.createObjectURL(target.files[0]));
    //e.target.value = ''; 
    return;
  }
  let src = URL.createObjectURL(target.files[0]);
  //let src = target.files[0];
  //document.getElementById('qna-img').setAttribute('src', e.target.result);

  let label=document.createElement('label');
  let image=document.createElement('img');
  let span=document.createElement('span');
  let icon=document.createElement('i');

  label.setAttribute('class', 'uploader-img');

  image.setAttribute('width', '100');
  image.setAttribute('id', 'qna-img-preview');
  image.setAttribute('src', src);

  icon.setAttribute('class', 'fa fa-trash fa-sm');
  span.setAttribute('class', 'trash');
  span.setAttribute('onclick', 'clearImage()')

  span.append(icon);
  label.append(image);
  label.append(span); 

  let parent=document.getElementById('uploaded_image');
  parent.insertBefore(label, parent.firstChild);

  //handle same file
  //e.target.value = ''; 
}

function clearImage(){
  let parent = document.getElementById('uploaded_image');
  parent.removeChild(parent.firstChild);
}

async function saveQuestion(){

  let formData = new FormData(document.getElementById('form-qna'));

  let category=document.getElementById('qna-cat').value;
  let title=document.getElementById('qna-title').value;
  let content=document.getElementById('qna-content').value;

  formData.append('qna-cat', category);
  formData.append('qna-title', title);
  formData.append('qna-content', content);

  const url = '/mypage/qna';
  const response = await fetch(url, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: formData
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();
  
  if(result.success){
    alert('문의가 성공적으로 등록되었습니다.');
    window.open('/mypage/qna-list', '_self');
  }
  else{
    alert('문의가 등록되지 않았습니다. 다시 작성해주시기 바랍니다.');
  }
}

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
    window.open('/mypage/qna-list', '_self');
  }
  else{
    alert('삭제되지 않았습니다. 다시 시도해주시기 바랍니다.');
    window.open('/mypage/qna-list', '_self');
  }
}