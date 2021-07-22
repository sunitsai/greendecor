(function($) {
    'use strict';
    $(function() {
      $('select').on('change', function() {
        var id = this.id;
        if(id.startsWith("id_onlinenerserycategory_set") && id.match('category')){
          var plants_from = id.replace('-category','-plants');
          var s_name = $('#'+plants_from);
          $.getJSON("/admin/getplants/",{id: this.value}, function(j){
              var options = '';
              for (var i = 0; i < j.length; i++) {
                options += '<option value="' + j[i].pk + '" >' + j[i].fields.name + '</option>';
              }
            $(s_name).html(options);
          })
        }
      })
    });
})(django.jQuery);
