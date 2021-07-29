

$('option').mousedown(function(e) {
  e.preventDefault();
  var originalScrollTop = $(this).parent().scrollTop();
  console.log(originalScrollTop);
  $(this).prop('selected', $(this).prop('selected') ? false : true);

  return false;
});

