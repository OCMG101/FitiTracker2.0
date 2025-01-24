// Display menu:
let menuList = document.getElementById("navRight");
menuList.style.maxHeight = "0px";

function toggleMenu() {
    if (menuList.style.maxHeight == "0px") {
        menuList.style.maxHeight = "300px";
    } else {
        menuList.style.maxHeight = "0px";
    }
}

// Icon change:
const toggle = document.getElementById('menu');
toggle.addEventListener('click', function () {
    this.classList.toggle('bi-x');
})
