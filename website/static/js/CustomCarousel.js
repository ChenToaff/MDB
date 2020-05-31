function CustomCarousel() {
  manageCarousel();

  $(".btn-prev, .btn-next").click(function () {
    moveCarousel(this);
  });
  $(window).resize(manageCarousel);
}
function manageCarousel() {
  $(".CustomCarousel").each(function () {
    resizeCarousel(this);
  });
}

//Resizes the items to fit custom division.
function spaced(carousel, parentWidth, items, pad) {
  const itemsSplit = $(carousel).attr("data-items").split(",");
  let visibleItems = itemsSplit[0];
  if (parentWidth >= 1200) {
    visibleItems = itemsSplit[4];
  } else if (parentWidth >= 992) {
    visibleItems = itemsSplit[3];
  } else if (parentWidth >= 768) {
    visibleItems = itemsSplit[2];
  } else if (parentWidth >= 576) {
    visibleItems = itemsSplit[1];
  }
  const itemWidth = (parentWidth - pad) / visibleItems;
  $(items).each(function () {
    $(this).outerWidth(itemWidth);
  });
}

//Resizes the carusel and sets items width.
function resizeCarousel(carousel) {
  const parentWidth = $(carousel).width();
  prevBtn = $(carousel).find(".btn-prev");
  nextBtn = $(carousel).find(".btn-next");
  prevBtn.hide();
  nextBtn.hide();

  let inner = $(carousel).find(".CustomCarousel-inner");
  const items = $(inner).find(".item");
  let pad = $(carousel).attr("data-padding");
  if (pad == NaN) pad = 0;
  else $(inner).css("padding-right", pad + "px");

  $(items).hide();
  let widthCount = 0 + parseInt(pad);
  let visibleItems = 0;
  if ($(carousel).hasClass("spaced")) {
    spaced(carousel, parentWidth, items, pad);
  }
  let last;
  let i = 0;
  $(items).each(function () {
    if (i > 0) $(this).css("padding-left", pad + "px");
    i++;
    $(this).removeClass("Last");
    widthCount += $(this).outerWidth();
    if (widthCount <= parentWidth) {
      visibleItems++;
      $(this).show();
      $(this).addClass("Visib");
      last = $(this);
    } else $(this).removeClass("Visib");
  });
  if (last) last.addClass("Last");

  if (items.length > visibleItems) {
    prevBtn.show();
    nextBtn.show();
  }
}

//Moves the items on button press.
function moveCarousel(btn) {
  const inner = $($(btn).parent()).find(".CustomCarousel-inner");
  let items = inner.find(".item");
  let visibleItems = inner.find(".item.Visib").length;
  let amount = visibleItems;
  if (items.length - visibleItems < visibleItems)
    amount = items.length - visibleItems;

  const condition = $(btn).hasClass("btn-prev");
  items.hide();
  //alert(amount);
  for (let i = 0; i < amount; i++) {
    items = inner.find(".item");
    if (condition) {
      items[0].before(items[items.length - 1]);
    } else {
      items[items.length - 1].after(items[0]);
    }
  }
  resizeCarousel(inner.parent());
}
