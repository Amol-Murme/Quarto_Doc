function save_edited(){
  const elements1 = document.querySelectorAll('[id^="editable_"]');

  elements1.forEach(element => {
    console.log(element.textContent.trim());
    console.log(element.id)
  });
}
