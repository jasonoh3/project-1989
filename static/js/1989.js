let doSubmit = function() {
  let e = document.getElementById("image");
  let f = e.files[0];

  var data = new FormData();
  data.append("image", f);
  
  fetch("/makeMosaic", {
    method: "POST",
    body: data
  })
  .then(response => response.json())
  .then(json => {
    let html = "";

    html += `<div class="row">`;
    for (let d of json) {
      html += `<div class="col-2"><img src="${d.image}" class="img-fluid"></div>`
    }
    html += `</div>`;

    let e = document.getElementById("mosaics");
    e.innerHTML = html;
  });
};