//Hamburger Menu//
const hamburger = document.querySelector('.hamburger')
const dropContent = document.querySelector('.dropdown-content')

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    dropContent.classList.toggle('active');
});

document.querySelectorAll('nav-item').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    dropContent.classList.remove('active');
}))

//Circle Animation//
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry)=> {
        console.log(entry)
        if(entry.isIntersecting){
            entry.target.classList.add('show');
            entry.target.classList.add('show2');
        }else{
            entry.target.classList.remove('show');
            entry.target.classList.remove('show2');
        }
    });
});

const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));

const hiddenElements2 = document.querySelectorAll('.hidden2');
hiddenElements2.forEach((el) => observer.observe(el));


//Dropdown Menus//
const selectBtn = document.getElementById('select-btn');
const selectBtn2 = document.getElementById('select-btn2');
const text = document.getElementById('text2');
const text3 = document.getElementById('text3');
const option = document.getElementsByClassName('option');
const option2 = document.getElementsByClassName('option2');


selectBtn.addEventListener('click', function() {
    selectBtn.classList.toggle('active');
});
selectBtn2.addEventListener('click', function() {
    selectBtn2.classList.toggle('active');
});


for(a of option) {
    a.onclick = function() {
        text.innerHTML = this.textContent;
        selectBtn2.classList.remove('active');
    }
}



