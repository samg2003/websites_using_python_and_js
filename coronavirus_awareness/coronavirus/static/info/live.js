document.addEventListener("DOMContentLoaded",()=>{
  document.querySelector("#form").onsubmit = () => {
    const request = new XMLHttpRequest();
    const country = document.querySelector("#country").value;
    request.open("POST", "{%url 'data'%}");

    request.onload = ()=>{

      const data = JSON.parse(request.responseText);
      if (data.success) {
                  var contents = `Country : ${data.country}`
                  document.querySelector('#resultcou').innerHTML = contents;
                  document.querySelector('#resultcou').style.display = 'block';
                  contents = `Confirmed Cases : ${data.confirmed}`
                  document.querySelector('#resultcon').innerHTML = contents;
                  document.querySelector('#resultcon').style.display = 'block';
                  contents = `Total Deaths : ${data.deaths}`
                  document.querySelector('#resultdea').innerHTML = contents;
                  document.querySelector('#resultdea').style.display = 'block';
                  contents = `Total Recovered : ${data.recovered}`
                  document.querySelector('#resultrec').innerHTML = contents;
                  document.querySelector('#resultrec').style.display = 'block';
                  contents = `Date Last Updated On : ${data.date}`
                  document.querySelector('#resultdat').innerHTML = contents;
                  document.querySelector('#resultdat').style.display = 'block';
              }
      else {
                  document.querySelector('#resultcou').innerHTML = 'Apology! Api is currently not working please try gain in 12 minutes!.';
      }

    };
    const data = new FormData();
    data.append('country', country);

        // Send request
    request.send(data);
    return false;
  };
});
