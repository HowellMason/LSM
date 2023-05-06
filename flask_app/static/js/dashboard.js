// BILL POPUP
document.querySelector("#add-bill-btn").addEventListener('click', function(){
    document.querySelector("#add-popup-bill").classList.add("active");
})
document.querySelector("#close-bill-popup").addEventListener('click', function(){
    document.querySelector("#add-popup-bill").classList.remove("active");
})

// INCOME POPUP
document.querySelector("#add-income-btn").addEventListener('click', function(){
    document.querySelector("#add-popup-income").classList.add("active");
})
document.querySelector("#close-income-popup").addEventListener('click', function(){
    document.querySelector("#add-popup-income").classList.remove("active");
})
