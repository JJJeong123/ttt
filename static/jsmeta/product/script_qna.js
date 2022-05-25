document.addEventListener("DOMContentLoaded", function(){
  let product_id=window.location.href.split("/").pop();
  console.log(product_id)

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
      'url': `/product/qna-table?product=${product_id}`,
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

            span.setAttribute('class', 'details-control');
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

  //Show content when title is clicked
  var detailRows = [];
 
  $('#dataTableHover-proqna tbody').on( 'click', 'tr .details-control', function () {
      var tr = $(this).closest('tr');
      var row = table_qna.row( tr );
      var idx = $.inArray( tr.attr('id'), detailRows );

      if ( row.child.isShown() ) {
          tr.removeClass( 'details' );
          row.child.hide();

          // Remove from the 'open' array
          detailRows.splice( idx, 1 );
      }
      else {
          tr.addClass( 'details' );
          row.child( format( row.data() ) ).show();

          // Add to the 'open' array
          if ( idx === -1 ) {
              detailRows.push( tr.attr('id') );
          }
      }
  });
  // On each draw, loop over the `detailRows` array and show any child rows
  table_qna.on( 'draw', function () {
      $.each( detailRows, function ( i, id ) {
          $('#'+id+' td.details-control').trigger( 'click' );
      });
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

  const title=document.getElementById('question-title').value;
  const content=document.getElementById('question-content').value;
  const isChecked=document.querySelector('.qna-checkbox>input').checked;
  
  const url = '/product/qna-post';
  const response = await fetch(url, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
        title: title,
        content: content,
        product_id: product_id,
        password: isChecked?'1':'0'
      })
  })
  .catch((error) => {
      alert(error);
  });

  const result = await response.json();

  if(result.success){
    
    alert('문의가 성공적으로 등록되었습니다.');
    closeModal();

    window.open('./'+product_id,'_self');
  }
  else{
    alert('문의가 등록되지 않았습니다. 다시 작성해주시기 바랍니다.');
  }
}

function format ( d ) {
  let parent=document.createElement('div');
  let p=document.createElement('p');
  
  p.setAttribute('align', 'left');
  p.setAttribute('class', 'mx-5 my-3');
  p.innerText=d.content;

  parent.append(p);

  if(d.answer_flag === '1'){
    let blockquote=document.createElement('blockquote');
    let div=document.createElement('div');
    let answer_content=document.createElement('p');

    blockquote.setAttribute('class', 'border-top my-3 pt-3 px-5');
    div.setAttribute('class', 'col mt-3');
    answer_content.setAttribute('align', 'left');
    answer_content.innerText=d.answer_content;

    div.append(answer_content);
    blockquote.append(div);
    parent.append(blockquote);
  }

  return parent.outerHTML;
}