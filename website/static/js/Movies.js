function fill_carousale(inner, data) {
  $(inner).html("");
  let item;
  for (let i = 0; i < data.length; i++) {
    item = $("<div/>", {
      id: data[i].imdbID,
      class: "item",
    });
    $("<img/>", {
      class: "moviePoster Poster",
      onclick: "getPlot(this.id)",
      id: data[i].imdbID,
      src: data[i].Poster,
    }).appendTo(item);
    $("<button/>", {
      style:
        "height:40px;width:40px;position:absolute;background-color:black;bottom:32px;left:3px;border:0;visibility:hidden;",
    }).appendTo(item);
    item.appendTo(inner);
  }
  resizeCarousel(inner.parent());
}
const userMovies = [];
function onLoad() {
  if ($("#topMoviesCaro").length) {
    axios.get("/movies/new").then((response) => {
      let d = response.data;
      if (d) {
        const inner = $("#topMoviesCaro").find(".CustomCarousel-inner");
        const data = JSON.parse(d);
        fill_carousale(inner, data);
      }
    });
  }
  if ($("#likedMoviesCaro").length) {
    axios
      .get("/user/liked/" + window.location.pathname.split("/").pop())
      .then((response) => {
        let d = response.data;
        if (d) {
          const inner = $("#likedMoviesCaro").find(".CustomCarousel-inner");
          const data = JSON.parse(d);
          fill_carousale(inner, data);
        }
      });
  }
}
async function getPlot(imdbID) {
  $("#overlayPoster").attr("src", "static/images/preloader3.gif");
  $("#overlayPlot").text("Loading...");
  $("#overlayTitle").text("Loading...");
  $("#likeImage").attr("src", "../static/images/before_like.png");
  openOverlay(imdbID);
  const response = await axios.get("/movie/" + imdbID, {
    headers: { JSON: 1 },
  });
  const movie = response.data;
  if (movie) {
    $("#overlayPoster").attr("src", movie.Poster);
    $("#overlayPlot").text(movie.Plot);
    $("#overlayTitle").text(movie.Title + " (" + movie.Year + ")");
    if (movie.Liked)
      $("#likeImage").attr("src", "../static/images/after_like.png");
  }
}

function likeBtn(img) {
  //$(this).css("pointer-events", "none");
  let imdbID = window.location.pathname.split("/");
  imdbID = imdbID[imdbID.length - 1];
  axios.get("/movies/like/" + imdbID).then((response) => {
    let d = response.data;
    if (d) {
      //$(this).css("pointer-events", "all");
      let src = $(img).attr("src");
      if (src.includes("after")) src = src.replace("after", "before");
      else src = src.replace("before", "after");
      $(img).attr("src", src);
      if ($("#topMoviesCaro").length) {
        onLoad();
      }
    }
  });
}
