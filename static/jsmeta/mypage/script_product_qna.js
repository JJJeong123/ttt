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
      'url': '/mypage/product_qna-table',
      'dataSrc': 'qna'
    },
    createdRow: function( row, data, dataIndex ) {
      $( row )
          .attr('onclick', "window.open('/mypage/product_qna-detail/"+data.id +"','_self');");
    },
    columnDefs: [
      {
        "targets": 0,
        "render": function (data) {
          return moment(data.created_at).format('YYYY.MM.DD');
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
      {data: 'product__name'},
      {data : 'title'},
      {data : null},
    ],
  });
});
