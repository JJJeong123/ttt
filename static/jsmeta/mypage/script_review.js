function setAttributes(el, attrs) {
    for(var key in attrs) {
      el.setAttribute(key, attrs[key]);
    }
}
  
document.addEventListener("DOMContentLoaded", function(){
  
    let table_reviewProduct = $('#dataTableHover-reviewProduct').DataTable({
      'destroy': true,
      'autoWidth': false,
  
      'ajax': {
        'type' : 'GET',
        'url': '/mypage/review-table',
        'dataSrc': 'reviewProduct'
      },
      columnDefs: [
        {
            "targets": 3,
            "render": function (data) {
                let td = document.createElement('td');
                td.setAttribute('class', 'align-middle');
                
                let btn_review = document.createElement('button');
                setAttributes(btn_review, {
                    'type': 'button',
                    'class': "btn btn-outline-primary pb-1",
                    'onclick':"location.href='/mypage/review-post/"+data.id+"'"
                });
                
                btn_review.innerText = '리뷰작성';
                td.appendChild(btn_review);
                return td.innerHTML;
            }
        },],
        
      columns: [
        {data : 'order__date'},
        {data : 'product__shop__shop_name'},
        {data : 'product__name'},
        {data : null},
      ],
    });
  
    let table_review = $('#dataTableHover-review').DataTable({
      'destroy': true,
      'autoWidth': false,
  
      'ajax': {
        'type' : 'GET',
        'url': '/mypage/review-table',
        'dataSrc': 'review'
      },
      createdRow: function( row, data, dataIndex ) {
        $( row )
            .attr('onclick', "window.open('/mypage/review-detail/"+data.id +"','_self')");
      },
      columns: [
        {data : 'created_at'},
        {data : 'orderproduct__product__shop__shop_name'},
        {data : 'orderproduct__product__name'},
        {data : 'rate'},
    ],
});
});




//delete product
/*
async function reviewPost(id) {
    const response = await fetch('review-post', {
      method: 'POST',
      headers: new Headers({
        'X-CSRFToken': getCookie('csrftoken'),
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        Id: id,
      }),
    }).catch((error) => {
      alert(error);
    });
  
    const result = await response.json();
  
    if(result.success){
        alert("상품이 삭제되었습니다");
        location.href='/management/product';
    }else{
        alert("error");
    }
}
*/