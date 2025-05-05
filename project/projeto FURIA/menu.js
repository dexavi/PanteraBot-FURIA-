
window.addEventListener("scroll", function(){
    let header = document.querySelector('#cabecalho')
    header.classList.toggle('rolagem',window.scrollY > 0)
})