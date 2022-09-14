function save_edited(){
  const elements1 = document.querySelectorAll('[id^="editable_"]');
  var edited_values = {};

  elements1.forEach(element => {
    id = element.id;
    key = id.replace("editable_", "");
    value = element.textContent.trim();

    edited_values[key] = value

  });

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
    },
    error: function(xhr, resp, text){
      console.log(xhr, resp, text)
    }

  });

  // console.log("Finished")
}
