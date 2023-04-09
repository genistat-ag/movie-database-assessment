(function($) {
  'use strict';

  if ($(".select2").length) {
    $(".select2").select2();
  }
  if ($(".select2-multiple").length) {
    $(".select2-multiple").select2();
  }
  $(".select2,select2-multiple").css("width", "100%")
})(jQuery);