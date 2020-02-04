const $flavor = $(".flavor");
const $size = $(".size");
const $rating = $(".rating");
const $image = $(".image");
const $cupcakeForm = $('#new-cupcake');
const $cupcakeList = $('#cupcake-list');



$cupcakeForm.on("submit", async function (evt) {
  
  evt.preventDefault();

  let flavor = $flavor.val();
  let size = $size.val();
  let rating = $rating.val();
  let image = $image.val();
  
  let resp = await axios.post("http://localhost:5000/api/cupcakes", {
    flavor,
    size,
    rating,
    image
  });

  let result = resp.data.cupcake;
  
  let cupcakeLi = $(`<li>${result.id}</li>`)
  $cupcakeList.append(cupcakeLi);
})