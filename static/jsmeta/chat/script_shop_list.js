document.addEventListener("DOMContentLoaded", function(){
    $('#dataTableHover-shop').dataTable({
      "bPaginate": true,
    });
    let table = $('#dataTableHover-shop').DataTable();
    
    $('#ShopCategoryId').on('change', function () {
      console.log(this.value);
      table.columns(1).search( this.value ).draw();
    });
    $('#ShopName').on('keyup', function () {
      table.columns(2).search( this.value ).draw();
    });
  });