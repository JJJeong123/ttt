//is on mobile
if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) { 
  $('#search').hide();
  $('#nav-mobile').show();

}
else {
  $('#search').show();
  $('#nav-mobile').hide();
}

