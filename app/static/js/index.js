function save_edited(){
  
  $('#loader').modal({
    backdrop: 'static',
    keyboard: false
  })
  $('#loader').modal('show');

  const elements1 = document.querySelectorAll('[id^="editable_"]');
  var edited_values = {};

  elements1.forEach(element => {
    // id = element.id;
    // key = id.replace("editable_", "");
    key = element.id
    value = element.textContent.trim();
    // value = value.replace(/(\r\n|\n|\r)/gm, "");
    value = value.replace(/(\s{3,})/gm, " **");
    value = value.replace(/(( \\_\s*|\\\n  \\|\\_))/gm, " ");

    edited_values[key] = value

  });

  console.log(edited_values)

  var temp = {
    "data" : edited_values
  }
  //  ajax call
  $.ajax({
    url:"/recompute",
    // async: true,
    type: "post",
    dataType: "json",
    contentType: "application/json",
    data: JSON.stringify(temp),
    success: function(res){
      console.log(res);
      console.log("Success")
      location.reload();
    },
    error: function(xhr, resp, text){
      console.log(xhr, resp, text)
    }

  });

  // console.log("Finished")
}
