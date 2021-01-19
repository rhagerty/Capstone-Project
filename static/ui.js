// ** age verification popup //

$(document).ready(function () {
  if (sessionStorage.getItem("ageVerify") !== "true") {
    $(".box").show();
    
  } else {
    $(".box").hide();
  }

  $(".enterPage").on("click", function () {
    $(".box").hide();
    sessionStorage.setItem("ageVerify", "true");
  });

  $(".exitPage").on("click", function () {
    $(".box").show();
    sessionStorage.setItem("ageVerify", "false");
  });

  $("#ingredientForm").hide();
  $("#nameForm").hide();
  $("#firstLetterForm").hide();
});

// Navigation search links//

$(".dropdown-btn").on("click", function () {
  $(".search-menu").toggle();
});

$(".ingredientNav").on("click", function () {
  $("#ingredientForm").toggle("slide");
});

$(".nameNav").on("click", function () {
  $("#nameForm").toggle("slide");
});

$(".firstLetterNav").on("click", function () {
  $("#firstLetterForm").toggle("slide");
});

$(".saveRecipe").on("click", function(){
  $(".saveRecipe").hide();
})