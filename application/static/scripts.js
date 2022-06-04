pular = 0;

window.onbeforeunload = function () {
    window.scrollTo(0, 0);
}

$(document).ready(function () {
    propostas_feed_container = document.getElementById('propostas_feed_container');

    if (propostas_feed_container != null) {
        arquivadas = document.getElementById("query_arquivada").value;

        jQuery.ajax({
            type: 'GET',
            url: `todas_propostas_nao_privadas?ordenar=recente&filtrar=todas&arquivadas=${arquivadas}`,
            success: function (response) {
                conteudo = ''
                response["propostas"].forEach(function(proposta) {
                    conteudo += proposta_card(proposta, response["user"]);
                    conteudo += proposta_modal_card(proposta, response["user"])
                });
    
                propostas_feed_container.innerHTML = conteudo;
                carregar_event_listeners_dinamicos();
                pular += 10;
            }
        });
    }
    
    $(function () {
        $.ajax({
            url: 'todos_usuarios'
        }).done(function (data) {
            $('#apelido_autocomplete').autocomplete({
                source: data,
                minLenght: 2
            })
        });
    });
    
    carregar_event_listeners_dinamicos();
    carregar_listeners_estaticos();
});


// Por favor Fran ignore tudo abaixo desta linha, só queria estar usando angular para mexer com
// dom, o importante é o backend
//______________________________________________________________________________________________
//

let icone_likear = function(proposta_ou_comentario, user) {
    likeou = false;
    likeadores = proposta_ou_comentario["likes"];
    for (i = 0; i < likeadores.length; i++) {
        if (likeadores[i]["id"] == user["id"]) {
            likeou = true;
        }
    };

    if (likeou) {
        return `<i class="bi bi-hand-thumbs-up-fill botao-like-proposta"></i> ${likeadores.length}`;
    }
    return `<i class="bi bi-hand-thumbs-up botao-like-proposta"></i> ${likeadores.length}`;
}


let data_criacao = function(proposta_ou_comentario) {
    conteudo = '';
    if (proposta_ou_comentario["dia_criacao"] < 10) {
        conteudo += `<h6 class="card-subtitle mb-2 text-muted lato-regular fs-6"style="text-align:start;">0${proposta_ou_comentario.dia_criacao}`;
    } else {
        conteudo += `<h6 class="card-subtitle mb-2 text-muted lato-regular fs-6"style="text-align:start;">${proposta_ou_comentario.dia_criacao}`;
    }
    if (proposta_ou_comentario["mes_criacao"] < 10) {
        conteudo += `/0${ proposta_ou_comentario.mes_criacao }/${proposta_ou_comentario.ano_criacao }</h6>`;
    } else {
        conteudo += `/${ proposta_ou_comentario.mes_criacao }/${proposta_ou_comentario.ano_criacao }</h6>`;
    }
    return conteudo;
}


let categorias = function(proposta) {
    conteudo = '';
    proposta["categorias"].forEach(function(categoria) {
        conteudo += `<h6 class="card-subtitle mb-2 text-muted categorias-proposta-item">${categoria.nome}</h6>`;
    })
    return conteudo;
}

let icone_favoritar = function(proposta, user) {
    favoritou = false;
    favoritadores = proposta["favoritadores"];
    for (i = 0; i < favoritadores.length; i++) {
        if (favoritadores[i]["id"] == user["id"]) {
            favoritou = true;
        }
    };

    if (favoritou) {
        return '<i class="bi bi-star-fill"></i> Remover favorito';
    }
    return '<i class="bi bi-star"></i> Favoritar';
}

let proposta_card = function(proposta, user) {return `<div id="${"id_item_feed_" + proposta.id}" class="card mx-auto mt-3 item-feed ${"bg-" + proposta.tipo_proposta}"><div class="card-top"style="text-align: start; padding: 16px 0 0 16px;"><form class="form_favoritar"><input type="hidden" name="proposta_id" value="${proposta.id}"><button class="botao-favoritar-proposta btn btn-primary" type="submit">${icone_favoritar(proposta, user)}</button></form></div><div class="card-body" style="padding-top: 5px;"><h5 class="card-title lato-bold fs-5" style="text-align: start;">${proposta.titulo}</h5>${data_criacao(proposta)}<div class="categorias-proposta">${categorias(proposta)}</div><p class="card-text lato-regular descricao-do-card" style="text-align: justify;">${proposta.descricao}</p><div class="comentar-participar-likear-feed"><form class="form_likear_proposta" style="margin-right: auto;"><input type="hidden" name="proposta_id" value="${proposta.id}"><button class="botao-likear-proposta btn" type="submit">${icone_likear(proposta, user)}</button></form><button type="button" class="card-link btn btn-info lato-bold " data-bs-toggle="modal"data-bs-target="#${"modal_comentarios_" + proposta.id}"style="margin-right: 5px;">Comentarios</button><form class="form_pedir_participar"><input type="hidden" value="${proposta.id}"><button type="submit" class="card-link btn btn-primary lato-bold solicitar_participar_butao" style="height: 100%; width: 100%;">Solicitar para participar</button></form></div></div></div>`}


let comentarios = function(comentarios, user) {
    conteudo = '';
    comentarios.forEach(function(comentario) {
        id_card_comentario = "id_card_comentario_" + comentario.id;
        conteudo += `<div class="card mx-auto mt-3 card_do_comentario" id="${id_card_comentario}"> <div class="card-body"> <h6 class="card-title lato-bold card_de_comentario_titulo fs-5"> <img class="comentario-foto" src="${comentario.user.foto_perfil}" alt="user"> ${comentario.dono_do_comentario} </h6> ${data_criacao(comentario)} <p class="card-text card_de_comentario_text lato-regular tamanho-padrao"> ${comentario.texto_comentario} </p> <div class="div-do-like"> <form class="form_likear_comentario"> <input type="hidden" name="comentario_id" value="${comentario.id}"> <button class="botao-likear-comentario btn" type="submit"> ${icone_likear(comentario, user)} </button> </form> </div> </div> </div>`
    });
    return conteudo;
}


let container_ordenar_comentario = function(proposta) {return `<div class="mr-auto mt-3 lato-regular"> <div class="div-ordenar-comentario" style="display: flex;"> <input type="hidden" name="proposta_id" value="${proposta.id}"> <div class="lato-regular input-de-ordenar" style="display: flex;"> Ordenar por: <div class="form-check" style="margin-left: 15px;"> <input class="form-check-input" type="radio" name="ordenar-comentario" checked id="recente_comentario" value="recente"> <label class="form-check-label lato-regular" for="recente"> Recente </label> </div> <div class="form-check" style="margin-left: 10px;"> <input class="form-check-input" type="radio" name="ordenar-comentario" id="popular_comentario" value="popular"> <label class="form-check-label lato-regular" for="popular"> Popular </label> </div> </div> </div> </div>`}


let proposta_modal_card = function(proposta, user) {return `<div class="modal fade modal-lg" id="${"modal_comentarios_" + proposta.id}" tabindex="-1" aria-hidden="true"> <div class="modal-dialog"><div class="modal-content"> <div class="modal-header"> <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button></div><div class="modal-body"> <form class="form_postar_comentario" novalidate> <div class="mb-2"> <input type="hidden" name="proposta_id" value="${proposta.id}"> <textarea class="form-control postar-comentario lato-regular fs-5" maxlength="1000" name="texto_comentario" placeholder="Comentário"></textarea> <span class="text-danger lato-bold postar_comentario_span fs-5" style="margin-top: 6px; margin-bottom: 5px;"></span></div> <button type="submit" class="botao-postar-comentario btn btn-info lato-bold fs-5" style="display: block; width: fit-content;">Comentar</button></form> ${container_ordenar_comentario(proposta)} <div class="mx-auto mt-3 comentarios_da_proposta">${comentarios(proposta.comentarios, user)}</div></div><div class="modal-footer"><button type="button"class="btn btn-secondary lato-bold"data-bs-dismiss="modal">Fechar</button></div></div></div></div>`;}


$(document).ready(function () {
    $('.div-ordenar-filtrar').on("change", function () {
        ordenar = $('#recente').prop('checked') ? "recente" : "popular";
        filtrar = document.getElementById("select_ordenar").value;
        arquivadas = document.getElementById("query_arquivada").value;

        jQuery.ajax({
            type: 'GET',
            url: `todas_propostas_nao_privadas?ordenar=${ordenar}&filtrar=${filtrar}&arquivadas=${arquivadas}`,
            success: function (response) {
                propostas_feed_container = document.getElementById('propostas_feed_container');
                conteudo = '';
                response["propostas"].forEach(function(proposta) {
                    conteudo += proposta_card(proposta, response["user"]);
                    conteudo += proposta_modal_card(proposta, response["user"])
                });
                propostas_feed_container.innerHTML = conteudo;
                carregar_event_listeners_dinamicos();
                pular += 10;
            }
        });
    });
});


// Event listeners
function carregar_event_listeners_dinamicos() {
    carregar_likear_proposta_listener();
    carregar_likear_comentario_listener();
    carregar_pedir_participar_listener();
    carregar_favoritar_listener();
    carregar_postar_comentario_listener();
    carregar_ordenar_comentario_listener();
}


function carregar_ordenar_comentario_listener() {
    $('.div-ordenar-comentario').on("change", function () {
        ordenar = $('#recente_comentario').prop('checked') ? "recente" : "popular";
        id_proposta = $(this).children('input')[0].value;
        modal_comentarios = $(this).parents('.modal');
        div_comentarios = modal_comentarios.find('.comentarios_da_proposta');

        jQuery.ajax({
            type: 'GET',
            url: `carregar_comentarios?id_proposta=${id_proposta}&ordenar=${ordenar}`,
            success: function (response) {
                div_comentarios.html(comentarios(response["comentarios"], response["user"]));
                carregar_likear_comentario_listener();
            }
        });
    });
}


function carregar_likear_proposta_listener() {
    $('.form_likear_proposta').submit(function ( event ) {
        event.preventDefault();
        id_proposta = $(this).children('input')[0].value;
        botao_do_like = $(this).children('button');

        $(function () {
            $.post(
                'likear_proposta',
                {
                    id_proposta: id_proposta
                },
                function (response) {
                    botao_do_like.html(icone_likear(response["proposta"], response["user"]));
                });
        });
    });
}


function carregar_likear_comentario_listener() {
    $('.form_likear_comentario').submit(function ( event ) {
        event.preventDefault();
        id_comentario = $(this).children('input')[0].value;
        botao_do_like = $(this).children('button');

        $(function () {
            $.post(
                'likear_comentario',
                {
                    id_comentario: id_comentario
                },
                function (response) {
                    botao_do_like.html(icone_likear(response["comentario"], response["user"]));
                });
        });
    });
}


function carregar_pedir_participar_listener() {
    $('.form_pedir_participar').submit(function (event) {
        event.preventDefault();
        id_proposta = $(this).children('input')[0].value;
    
        $(function () {
            $.post(
                'participar',
                {
                    id_proposta: id_proposta
                },
                function (response) {
                    let codigo = response["status"];
    
                    if (codigo == 400) {
                        let liveToast = $('.toast-erro');
                        liveToast.find('.toast-body').text(response["mensagem"]);
                        let toast = new bootstrap.Toast(liveToast);
                        
                        toast.show();
                        return
                    }
    
                    if (codigo == 200) {
                        let liveToast = $('.toast-sucesso');
                        liveToast.find('.toast-body').text(response["mensagem"]);
                        let toast = new bootstrap.Toast(liveToast);
                        
                        toast.show();
                        return
                    }
                });
        });
    });
}

function carregar_favoritar_listener() {
    $('.form_favoritar').submit(function( event ) {
        event.preventDefault();
        id_proposta = $(this).children('input')[0].value;
        botao_do_favorito = $(this).children('button');

        $(function () {
            $.post(
                'favoritar',
                {
                    id_proposta: id_proposta
                },
                function (response) {
                    if (response["status"] == 400) {
                        let liveToast = $('.toast-erro');
                        liveToast.find('.toast-body').text(response["mensagem"]);
                        let toast = new bootstrap.Toast(liveToast);
                        
                        toast.show();
                        return
                    }

                    
                    let liveToast = $('.toast-padrao');
                    liveToast.find('.toast-body').text(response["mensagem"]);
                    let toast = new bootstrap.Toast(liveToast);
                    
                    toast.show();
                    
                    botao_do_favorito.html(icone_favoritar(response["proposta"], response["user"]));
                });
        });
    });
}


function carregar_postar_comentario_listener() {
    $('.form_postar_comentario').submit(function ( event ) {
        event.preventDefault();
        comentario = $(this).children('div').children('textarea')[0].value;
        proposta_id = $(this).children('div').children('input')[0].value;
        comentar_span = $(this).children('div').children('span');
        comentar_area = $(this).children('div').children('textarea');
        modal_comentarios = $(this).parents('.modal');
        div_comentarios = modal_comentarios.find('.comentarios_da_proposta');
        
        $(function () {
            $.post(
                'criar_comentario',
                {
                    texto_comentario: comentario,
                    id_proposta: proposta_id
                },
                function (response) {
                    if (response["status"] == 400) {
                        comentar_span.text(
                            response["mensagem"]
                        );
                        return;
                    }

                    if (response["status"] == 100) {
                        div_comentarios.innerHTML = `<h3>${response["info"]}</h3>`
                    }
    
                    comentar_span.text("");
                    comentar_area.val("");
                    
                    div_comentarios.html(comentarios(response["comentarios"], response["user"]));
                    carregar_likear_comentario_listener();
                });
        });
    });
}


function carregar_on_click_para_botao(membros) {
    $('.x-remover-membro').on("click", function () {
        membro = $(this).siblings('.membros_lista_azul').text();

        for (i = 0; i < membros.length; i++) {
            if (membros[i] == membro) {
                membros.splice(i);
            }
        }

        inputs_invisiveis = $('#div_invisivel_membros').children('input');

        for (i=0; i < inputs_invisiveis.length; i++) {
            if (inputs_invisiveis[i].defaultValue == membro) {
                inputs_invisiveis[i].remove();
            }
        }

        $(this).siblings('.membros_lista_azul').css({"background-color": "red"});
        $(this).remove();
    });
}


function carregar_adicionar_membro_listener() {
    var membros = [];

    inputs_invi = $('#div_invisivel_membros').children('input');
    for (i = 0; i < inputs_invi.length; i++) {
        membros.push(inputs_invi[i].defaultValue)
    }

    carregar_on_click_para_botao(membros);

    $('#adicionar_membro_btn').on("click", function () {
        membro = $('#apelido_autocomplete').val();

        jQuery.ajax({
            url: 'checar_usuario',
            data: {
                apelido: membro
            },
            success: function (response) {
                // Validação
                if (response["status"] != 200) {
                    $('#adicionar_membro_span').text(response["mensagem"]);
                    return
                }
    
                // Limpar campo de membro
                $('#apelido_autocomplete').val("")
    
                // Validação
                if (membros.includes(response["mensagem"])) {
                    $('#adicionar_membro_span').text("Usuário já adicionado");
                    return
                }
    
                // limpar mensagem de erro
                $('#adicionar_membro_span').text("");
    
                membros.push(response["mensagem"]);
    
                aleatorio = (Math.floor(Math.random() * 3)) + 1
    
                classe_aleatoria = aleatorio == 1 ? "membros_lista_amarelo" : aleatorio == 2 ? "membros_lista_azul" : aleatorio == 3 ? "membros_lista_bege" : "membros_lista";
    
                if ($('#lista_de_membros').children('div').length > 0) {
                    divs_antigas = $('#lista_de_membros').html();
                    nova_div_membro = `<div class="margem-direita"><li class="${classe_aleatoria}">${response["mensagem"]}</li><a class="lato-bold x-remover-membro">X</a></div>`;
                    divs_antigas += nova_div_membro;
                    $('#lista_de_membros').html(divs_antigas);
                }
                else {
                    listas_antigas = $('#lista_de_membros').html();
                    nova_lista_item_membro = `<li class="${classe_aleatoria}">${response["mensagem"]}</li>`;
                    listas_antigas += nova_lista_item_membro;
                    $('#lista_de_membros').html(listas_antigas);
                }
    
                inputs_antigos = $('#div_invisivel_membros').html();

                membros.forEach(membro => {
                    input_novo = `<input type="hidden" name="membros" value="${membro}">`
                    inputs_antigos += input_novo;
                });

                $('#div_invisivel_membros').html(inputs_antigos);
    
                carregar_on_click_para_botao(membros);
            }});
    });

}


function carregar_listeners_estaticos() {
    // Listeners estaticos da página
    $('.notification-ui_icon').on('click', function () {
        mostrar = "dropdown-menu notification-ui_dd show";
        esconder = "dropdown-menu notification-ui_dd hide";
        notificacao = document.querySelector('.notification-ui_dd');

        if (notificacao.className == mostrar) {
            notificacao.className = esconder;
            return
        }
        notificacao.className = mostrar;
    });

    $('.form_aprovar_participacao').submit(function (event) {
        event.preventDefault();
        input_quem_pediu = $(this).find('.input_quem_pediu')[0].value;
        id_proposta = $(this).find('.input_proposta_id')[0].value;
        notificacao = $(this).parents('.notification-list');

        $(function () {
            $.post(
                'aprovar_participacao',
                {
                    quem_pediu_para_entrar: input_quem_pediu,
                    proposta_id: id_proposta
                },
                function (response) {
                    let codigo = response["codigo"];
    
                    if (codigo == 200) {
                        notificacao.remove();
                        let liveToast = $('.toast-sucesso');
                        liveToast.find('.toast-body').text("Usuário adicionado a proposta");
                        let toast = new bootstrap.Toast(liveToast);
                        
                        toast.show();
                        return
                    }
                });
            fechar_notificacoes_se_nenhuma();
        });
    });
    
    $('.form_recusar_participacao').submit(function (event) {
        event.preventDefault();
        input_quem_pediu = $(this).find('.input_quem_pediu')[0].value;
        id_proposta = $(this).find('.input_proposta_id')[0].value;
        notificacao = $(this).parents('.notification-list');

        $(function () {
            $.post(
                'recusar_participacao',
                {
                    quem_pediu_para_entrar: input_quem_pediu,
                    proposta_id: id_proposta
                },
                function (response) {
                    notificacao.remove();
                });
            fechar_notificacoes_se_nenhuma();
        });
    });

    $(window).scroll(function() {
        if($(window).scrollTop() + $(window).height() >= $("#feed_container").height()) {
            ordenar = $('#recente').prop('checked') ? "recente" : "popular";
            filtrar = document.getElementById("select_ordenar").value;
            arquivadas = document.getElementById("query_arquivada").value;


            jQuery.ajax({
                type: 'GET',
                url: `todas_propostas_nao_privadas?ordenar=${ordenar}&filtrar=${filtrar}&arquivadas=${arquivadas}&pular=${pular}`,
                success: function (response) {
                    propostas_feed_container = document.getElementById('propostas_feed_container');
                    conteudo_anterior = propostas_feed_container.innerHTML;
                    response["propostas"].forEach(function(proposta) {
                        conteudo_anterior += proposta_card(proposta, response["user"]);
                        conteudo_anterior += proposta_modal_card(proposta, response["user"])
                    });
                    propostas_feed_container.innerHTML = conteudo_anterior;
                    carregar_event_listeners_dinamicos();
                }
            });

            pular += 10;
        }
    });

    carregar_adicionar_membro_listener();
}


// Funções auxiliares
function fechar_notificacoes_se_nenhuma() {
    container_de_notificacoes = document.querySelector('.notification-ui_dd-content');
    container_do_container_de_notifi = document.querySelector('.notification-ui_dd');
    mostrar = "dropdown-menu notification-ui_dd show";
    esconder = "dropdown-menu notification-ui_dd hide";

    console.log(container_de_notificacoes.children.length);
    console.log(container_de_notificacoes.children);
    if (container_de_notificacoes.children.length <= 1) {
        container_do_container_de_notifi.className = esconder;
    }
}

function formatar_baseado_em_largura() {
    if ($(window).width() < 600) {
        $('#toggle-item-feed-postar').css("display", "inline-block");
        $('#toggle-item-feed-postar').css("height", "38px");
        $('.item-feed-postar').css("display", "none");
    } else {
        $('#toggle-item-feed-postar').css("display", "none");
        $('#toggle-item-feed-postar').css("height", "0px");
        $('.item-feed-postar').css("display", "flex");
    }
}

$(document).ready(function () {
    formatar_baseado_em_largura();
});

$(window).resize(function () {
    formatar_baseado_em_largura();
});

$(document).ready(function () {
    $('#toggle-item-feed-postar').on("click", function () {
        $('#toggle-item-feed-postar').css("display", "none");
        $('.item-feed-postar').css("display", "flex");
    });
});