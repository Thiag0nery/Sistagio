const getElement = (...queries) => document.querySelector(...queries);

    elemento = document.querySelectorAll('.itens-card-vagas');
    var btn_exlcuir_vaga = document.querySelectorAll('.btn-exlcuir-vaga');

    var modal = getElement(".modal-container");


    activeModalClass = 'modal-show';

    elemento.forEach(function (elements) {
        elements.addEventListener('click', function () {
            showModal(elements);
            var candidatos = document.getElementById('candidatos') // Busca elemento
            var paragrafo = document.createElement("p") // Criar elemento
            var paragrafo_existentes = candidatos.querySelectorAll("p"); // Selecionar todos os paragrafos
            for (var i = 0; i < paragrafo_existentes.length; i++) {
              candidatos.removeChild(paragrafo_existentes[i]);
            }
            excluirvaga(elements)
             $(document).ready(function() {
  var urlRequisicao = $('#urlRequisicao').data('url');
       $.ajax({
                    url: urlRequisicao,
                    type: 'POST',
                    data: {
                        'vaga_codigo': document.getElementById('id-vaga').innerHTML
                    },
                    success: function(data) {
                    //Verificação se tem algum candidato na vaga, ele gera um erro quando não e tratado
                    try {
                        for (var i = 0; i < Object.keys(data).length; i++) {
                        paragrafo.textContent = data.data[i].nome;
                        candidatos.appendChild(paragrafo)
                        }
                    }
                    catch (e) {
                        paragrafo.textContent = 'Nenhum canditado inscrito';
                        candidatos.appendChild(paragrafo)
                    }


                    }
                });

});//fim ajax

    })
    })

    function showModal(element) {
        var nome = element.querySelector("h2");
        var nome_empresa = element.querySelector("h3");
        var endereco = element.querySelector("h5");
        var vaga_descricao = element.querySelector("vaga_descricao");
        var vaga_funcao = element.querySelector("vaga_funcao");
        var vaga_beneficio = element.querySelector("vaga_beneficio");
        var vaga_codigo = element.querySelector("vaga_codigo");


        document.getElementById("vaga-nome").innerHTML = nome.innerHTML;
        document.getElementById("vaga-funcao").innerHTML = vaga_funcao.innerHTML;
        document.getElementById("vaga-beneficio").innerHTML = vaga_beneficio.innerHTML;
        document.getElementById("vaga-descricao").innerHTML = vaga_descricao.innerHTML;
        document.getElementById("empresa-nome").innerHTML = nome_empresa.innerHTML;
        document.getElementById("empresa_endereco").innerHTML = endereco.innerHTML;
        document.getElementById("id-vaga").innerHTML = vaga_codigo.innerHTML;

        modal.classList.add(activeModalClass)
    }


    modal.addEventListener('click', (event) => {
        modal.classList.remove(activeModalClass)
    })
containerVagas = document.getElementById('card-vagas')
function excluirvaga(div){
     btn_exlcuir_vaga.forEach(function (elements) {
        elements.addEventListener('click', function () {
        var saida = confirm('Dejesa excluir vaga?')

        if (saida == true) {
               var vaga_codigo =  document.getElementById("id-vaga").innerHTML;



             $(document).ready(function() {
  var urlExcluirvaga = $('#urlExcluirvaga').data('url');
       $.ajax({
                    url: urlExcluirvaga,
                    type: 'POST',
                    data: {
                        'vaga_codigo': document.getElementById('id-vaga').innerHTML
                    },
                    success: function(data) {
                    //Verificação se tem algum candidato na vaga, ele gera um erro quando não e tratado

                     containerVagas.removeChild(div)
                     console.log(data.certo)




                    }
                });

});//fim ajax
        }



        })

    })
}

