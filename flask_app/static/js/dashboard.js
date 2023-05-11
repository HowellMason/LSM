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

// DAILY POPUP
document.querySelector("#add-daily-btn").addEventListener('click', function(){
    document.querySelector("#add-popup-daily").classList.add("active")
})
document.querySelector("#close-daily-popup").addEventListener('click', function(){
    document.querySelector("#add-popup-daily").classList.remove("active");
})

// WEEKLY POPUP
document.querySelector("#add-weekly-btn").addEventListener('click', function(){
    document.querySelector("#add-popup-weekly").classList.add("active")
})
document.querySelector("#close-weekly-popup").addEventListener('click', function(){
    document.querySelector("#add-popup-weekly").classList.remove("active");
})