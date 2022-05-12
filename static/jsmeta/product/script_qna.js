document.addEventListener("DOMContentLoaded", function(){

  let table_qna = $('#dataTableHover-proqna').DataTable({
    destroy: true,
    autoWidth: false,
    searching: false,
    dom: 'rtip',
    paging: false,
    order: [[ 0, "desc" ]],
    info: false,

    ajax: {
      'type' : 'GET',
      'url': '/product/qna-table',
      'dataSrc': 'qna'
    },
    columnDefs: [
      {
        "targets": 0,
        "render": function (data) {
          return moment(data.created_at).format('YYYY.MM.DD');
        }
      },
      {
        "targets": 1,
        "render": function (data) {
          let span=document.createElement('span');

          if(data.password==='0'){

            span.setAttribute('onclick', "window.open('/mypage/product_qna-detail/"+data.id +"','_self');");
            span.innerText=data.title;

            return span.outerHTML;
          }
          span.setAttribute('class', 'text-muted');
          span.innerText="비밀글입니다.";

          return span.outerHTML;
        }
      },
      {
          "targets": 3,
          "render": function (data) {
            let span=document.createElement('span');
            if(data.answer_flag==='0') {
              span.setAttribute('style', 'color: #1c5d1c; font-weight: bold;');
              span.innerText='미답변';
            }
            else {
              span.setAttribute('style', 'font-weight: bold;');
              span.innerText='답변완료';
            }
            return span.outerHTML;
          }
      },
    ],
    columns: [
      {data : null},
      {data : null},
      {data : 'member__mem_name'},
      {data : null},
    ],
  });
});

function openModal(){
  $('#qna-add').modal('show');
}

function openLoginModal(){
  $('#login').modal('show');
}

function closeModal(){
  $('#qna-add').modal('hide');
}

function closeLoginModal(){
  $('#login').modal('hide');
  window.open('../../login','_self');
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

    $('#dataTableHover-proqna').DataTable({
      destroy: true,
      autoWidth: false,
      searching: false,
      dom: 'rtip',
      paging: false,
      order: [[ 0, "desc" ]],
      info: false,
  
      ajax: {
        'type' : 'GET',
        'url': '/product/qna-table',
        'dataSrc': 'qna'
      },
      columnDefs: [
        {
          "targets": 0,
          "render": function (data) {
            return moment(data.created_at).format('YYYY.MM.DD');
          }
        },
        {
          "targets": 1,
          "render": function (data) {
            let span=document.createElement('span');
  
            if(data.password==='0'){
              
              span.setAttribute('onclick', "window.open('/mypage/product_qna-detail/"+data.id +"','_self');");
              span.innerText=data.title;
  
              return span.outerHTML;
            }
            span.setAttribute('class', 'text-muted');
            span.innerText="비밀글입니다.";
  
            return span.outerHTML;
          }
        },
        {
            "targets": 3,
            "render": function (data) {
              let span=document.createElement('span');
              if(data.answer_flag==='0') {
                span.setAttribute('style', 'color: #1c5d1c; font-weight: bold;');
                span.innerText='미답변';
              }
              else {
                span.setAttribute('style', 'font-weight: bold;');
                span.innerText='답변완료';
              }
              return span.outerHTML;
            }
        },
      ],
      columns: [
        {data : null},
        {data : null},
        {data : 'member__mem_name'},
        {data : null},
      ],
    });
  }
  else{
    alert('문의가 등록되지 않았습니다. 다시 작성해주시기 바랍니다.');
  }

}