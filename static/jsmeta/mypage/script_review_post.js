function addImage(e){
  e = e || window.event;
  let target = e.target || e.srcElement;

  if(document.getElementById('review-img-preview')){
    document.getElementById('review-img-preview').setAttribute('src', URL.createObjectURL(target.files[0]));
    //e.target.value = ''; 
    return;
  }
  let src = URL.createObjectURL(target.files[0]);
  
  let label=document.createElement('label');
  let image=document.createElement('img');
  let span=document.createElement('span');
  let icon=document.createElement('i');

  label.setAttribute('class', 'uploader-img');

  image.setAttribute('width', '100');
  image.setAttribute('id', 'review-img-preview');
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

async function saveReview(orderproduct_id){

  let formData = new FormData(document.getElementById('form-review'));

  let rate=document.getElementById('review-rate').value;
  let content=document.getElementById('review-content').value;
  
  formData.append('review-id', orderproduct_id);
  formData.append('review-rate', rate);
  formData.append('review-content', content);

  const url = '/mypage/review';
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
    alert('후기가 성공적으로 작성되었습니다.');
    window.open('/mypage/review', '_self');
  }
  else{
    alert('후기가 등록되지 않았습니다. 다시 작성해주시기 바랍니다.');
  }

}