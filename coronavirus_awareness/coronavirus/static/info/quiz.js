document.addEventListener("DOMContentLoaded",() =>{
  document.querySelectorAll(".answer-save").forEach(function(button){
    button.onclick = function(){
      let data = button.dataset.id;
      let search = "#" + data;
      let answer = document.querySelector(search).value;
      localStorage.setItem(data,answer);
    };
  });

  document.querySelectorAll(".form-control").forEach(function(select){
    let search = select.id;
    if (localStorage.getItem(search)){
      let answer = localStorage.getItem(search);
      select.value = answer
    }
  });

});
