const btnSubmit = document.getElementById('btnSubmit');


document.getElementById('mainImg').onchange = function () {
  let file = $('#mainImg')[0].files[0];
  if (file){
    document.getElementById('mainImg-label').innerText=file.name;
  }
};



let input = document.getElementById("mainImg"),
preview = document.getElementById("preview");
    
input.addEventListener("change", function() {
  changeImage(this);
});

function changeImage(input) {
  let reader;

  if (input.files && input.files[0]) {
    reader = new FileReader();

    reader.onload = function(e) {
      preview.setAttribute('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]);
    
    document.getElementById('mainImg-label').innerText=input.files[0].name;
  }
}

btnSubmit.addEventListener('click', async() => {
    const formData = new FormData(document.getElementById('uploadImgForm'));
    formData.append('rate', document.getElementById('rate').value);
    formData.append('content', document.getElementById('content').value);
    formData.append('orderProId', document.getElementById('orderProId').value);

    console.log(content);
   
    const response = await fetch('review-post', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: formData,
    })
    .catch((error) => {
        alert(error);
    })

    const result = await response.json()
    if (result.success){
        alert("리뷰가 등록되었습니다.");
        location.href='/mypage/review';
    }
})
