var form_alterar = document.getElementById('form-alterar')
var form_fisico = document.getElementById('form-dados-banco')
document.getElementById('btn-alterar').addEventListener('click', function(){
    form_alterar.style.display = 'block'
    form_fisico.style.display = 'none'
});
document.getElementById('btn-salvar').addEventListener('click', function(){
    form_alterar.style.display = 'none'
    form_fisico.style.display = 'block'
});

document.getElementById('logout_header').addEventListener('click', function(){
    var saida = confirm('Dejesa sair do sistema?')
    console.log(saida)
    if (saida == true) {
        window.location.href = "/logout"
    }
});