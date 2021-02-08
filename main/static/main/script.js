var important = document.querySelectorAll(".far");

for (var i = 0; i < important.length; i++) {
    important[i].addEventListener("click", function () {
        important[0].classList.toggle("fas")
    });
}