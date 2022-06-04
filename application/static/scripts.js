$(document).ready(function () {
    carregar_event_listeners();


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
                    if (JSON.parse(response)["likeado"]) {
                        botao_do_like.text("");
                        var novo_icone = $("<i>", {
                            class:
                                "bi-hand-thumbs-up-fill botao-like-comentario"
                        });
                    } else {
                        botao_do_like.text("");
                        var novo_icone = $("<i>", {
                            class:
                                "bi-hand-thumbs-up botao-like-comentario"
                        });
                    }

                    texto = document.createTextNode(" " + JSON.parse(response)["numeros_de_like"] + " ");
                    botao_do_like.append(novo_icone);
                    botao_do_like.append(texto);
                });
        });
    });

    $('.form_likear_comentario').submit(function ( event ) {
        event.preventDefault();
        likear_comentario(this);
    });

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
                    if (JSON.parse(response)["status"] == 400) {
                        let liveToast = $('.toast-erro');
                        liveToast.find('.toast-body').text(JSON.parse(response)["mensagem"]);
                        let toast = new bootstrap.Toast(liveToast);
                        
                        toast.show();
                        return
                    }

                    novo_icone = null;
                    texto = null;
                    if (JSON.parse(response)["favoritado"]) {
                        botao_do_favorito.text("");
                        novo_icone = $("<i>", {
                            class:
                                "bi-star-fill"
                        });
                        texto = document.createTextNode(" " + "Remover dos favoritos" + " ");
                    } else {
                        botao_do_favorito.text("");
                        novo_icone = $("<i>", {
                            class:
                                "bi-star"
                        });
                        texto = document.createTextNode(" " + "Favoritar" + " ");
                    }
                    
                    botao_do_favorito.append(novo_icone);
                    botao_do_favorito.append(texto);
                    
                    let liveToast = $('.toast-padrao');
                    liveToast.find('.toast-body').text(JSON.parse(response)["mensagem"]);
                    let toast = new bootstrap.Toast(liveToast);
                    
                    toast.show();
                });
        });
    });

    $('.form_postar_comentario').submit(function ( event ) {
        event.preventDefault();
        comentario = $(this).children('div').children('textarea')[0].value;
        proposta_id = $(this).children('div').children('input')[0].value;
        comentar_span = $(this).children('div').children('span');
        comentar_area = $(this).children('div').children('textarea');
        modal_comentarios = $(this).parents('.modal');
    
        $(function () {
            $.post(
                'comentar',
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
    
                    comentar_span.text("");
                    comentar_area.val("");

                    carregar_comentarios(response, modal_comentarios);
                });
        });
    });
});

function likear_comentario(trigger) {
    id_comentario = $(trigger).children('input')[0].value;
        botao_do_like = $(trigger).children('button');

        $(function () {
            $.post(
                'likear_comentario',
                {
                    id_comentario: id_comentario
                },
                function (response) {
                    novo_icone = null
                    if (JSON.parse(response)["likeado"]) {
                        botao_do_like.text("");
                        novo_icone = $("<i>", {
                            class:
                                "bi-hand-thumbs-up-fill botao-like-comentario"
                        });
                    } else {
                        botao_do_like.text("");
                        novo_icone = $("<i>", {
                            class:
                                "bi-hand-thumbs-up botao-like-comentario"
                        });
                    }

                    texto = document.createTextNode(" " + JSON.parse(response)["numeros_de_like"] + " ");
                    botao_do_like.append(novo_icone);
                    botao_do_like.append(texto);
                });
        });
}

function carregar_comentarios(comentarios, modal_comentarios) {
    div_comentarios = modal_comentarios.find('.comentarios_da_proposta');
    div_comentarios.empty();
    comentarios.forEach((comentario) => {
        console.log(comentario);

        var card_de_comentario = $("<div>", {
            id: "comentario" + comentario["id"],
            class: "card mx-auto mt-3",
        });

        var card_de_comentario_body = $("<div>", {
            id: "comentario_corpo_" + comentario["id"],
            class: "card-body",
        });

        var card_de_comentario_titulo = $("<h6>", {
            id: "comentario_titulo_" + comentario["id"],
            class: "card-title gothic-bold card_de_comentario_titulo",
        });

        var card_de_comentario_subtitulo = $("<p>", {
            id: "comentario_subtitulo_" + comentario["id"],
            class:
                "card-subtitle mb-2 text-muted gothic card_de_comentario_subtitulo",
        });

        if (comentario["mes_criacao"] < 10) {
            card_de_comentario_subtitulo.append(
                `${comentario["dia_criacao"]}/0${comentario["mes_criacao"]}/${comentario["ano_criacao"]}`
            );
        } else {
            card_de_comentario_subtitulo.append(
                `${comentario["dia_criacao"]}/${comentario["mes_criacao"]}/${comentario["ano_criacao"]}`
            );
        }

        var card_de_comentario_text = $("<p>", {
            id: "comentario_text_" + comentario["id"],
            class: "card-text card_de_comentario_text tamanho-padrao",
        });

        var card_de_comentario_foto = $("<img>", {
            class: "comentario-foto",
            src: comentario["user"]["foto_perfil"]
        });

        card_de_comentario_text.append(comentario["texto_comentario"]);
        card_de_comentario_titulo.append(card_de_comentario_foto);
        card_de_comentario_titulo.append(comentario["dono_do_comentario"]);
        card_de_comentario_body.append(card_de_comentario_titulo);
        card_de_comentario_body.append(card_de_comentario_subtitulo);
        card_de_comentario_body.append(card_de_comentario_text);
        card_de_comentario.append(card_de_comentario_body);
        div_comentarios.append(card_de_comentario);

        var div_do_like = $("<div>", { class: "div-do-like" });

        var form_do_like = $("<form>", { class: "form_likear_comentario" });

        var input_do_comentario_id = $("<input>", { type: "hidden", value: comentario["id"] });

        var botao_do_like = $("<button>", { class: "botao-likear-comentario btn" });

        var classe_do_icone = comentario["likeado"] ? "bi bi-hand-thumbs-up-fill botao-like-comentario" : "bi bi-hand-thumbs-up botao-like-comentario";

        var icone_do_like = $("<i>", { class: classe_do_icone });

        form_do_like.submit(function ( event ) {
            event.preventDefault();
            likear_comentario(this);
        });
        
        botao_do_like.append(icone_do_like);
        form_do_like.append(input_do_comentario_id);
        form_do_like.append(botao_do_like);
        div_do_like.append(form_do_like);
        card_de_comentario_body.append(div_do_like);

        texto = document.createTextNode(" " + comentario["likes"].length + " ");
        botao_do_like.append(texto);
    });
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

$(document).ready(function () {
    var membros = [];

    inputs_invi = $('#div_invisivel_membros').children('input');
    for (i = 0; i < inputs_invi.length; i++) {
        membros.push(inputs_invi[i].defaultValue)
    }

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
                    var $list = $("<li>", { "class": classe_aleatoria });
                    $list.append(response["mensagem"]);
                    var $div_membro = $("<div>", { "class": "margem-direita" });
                    var $anchor_remover_membro = $("<a>", { "class": "lato-bold x-remover-membro" });
                    $anchor_remover_membro.append("X");
                    $div_membro.append($list);
                    $div_membro.append($anchor_remover_membro);
                    $('#lista_de_membros').append($div_membro);
                }
                else {
                    var $list = $("<li>", { "class": classe_aleatoria });
                    $list.append(response["mensagem"]);
                    $('#lista_de_membros').append($list);
                }
                
                $('#div_invisivel_membros').text("");
                membros.forEach(element => {
                    $('<input>').attr({
                        type: 'hidden',
                        name: 'membros',
                        value: element
                    }).appendTo('#div_invisivel_membros');
                });
                carregar_on_click_para_botao(membros);
            }
        })
    });

    carregar_on_click_para_botao(membros);
});

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


// Por favor Fran ignore tudo abaixo desta linha, só queria estar usando angular para mexer com dom, o importante é o backend
//______________________________________________________________________________________________
//

let icone_likear = function(item, user) {
    likeou = false;
    likeadores = item["likes"];
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


let data_criacao = function(item) {
    conteudo = '';
    if (item["dia_criacao"] < 10) {
        conteudo += `<h6 class="card-subtitle mb-2 text-muted lato-regular fs-6"style="text-align:start;">0${item.dia_criacao}`;
    } else {
        conteudo += `<h6 class="card-subtitle mb-2 text-muted lato-regular fs-6"style="text-align:start;">${item.dia_criacao}`;
    }
    if (item["mes_criacao"] < 10) {
        conteudo += `/0${ item.mes_criacao }/${item.ano_criacao }</h6>`;
    } else {
        conteudo += `/${ item.mes_criacao }/${item.ano_criacao }</h6>`;
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

let proposta_card = function(proposta, user, id_item_feed, classe_background, id_modal_comentarios) {return `<div id="${id_item_feed}" class="card mx-auto mt-3 item-feed ${classe_background}"><div class="card-top"style="text-align: start; padding: 16px 0 0 16px;"><form class="form_favoritar"><input type="hidden" name="proposta_id" value="${proposta.id}"><button class="botao-favoritar-proposta btn btn-primary" type="submit">${icone_favoritar(proposta, user)}</button></form></div><div class="card-body" style="padding-top: 5px;"><h5 class="card-title lato-bold fs-5" style="text-align: start;">${proposta.titulo}</h5>${data_criacao(proposta)}<div class="categorias-proposta">${categorias(proposta)}</div><p class="card-text lato-regular descricao-do-card" style="text-align: justify;">${proposta.descricao}</p><div class="comentar-participar-likear-feed"><form class="form_likear_proposta" style="margin-right: auto;"><input type="hidden" name="proposta_id" value="${proposta.id}"><button class="botao-likear-proposta btn" type="submit">${icone_likear(proposta, user)}</button></form><button type="button" class="card-link btn btn-info lato-bold " data-bs-toggle="modal"data-bs-target="#${id_modal_comentarios}"style="margin-right: 5px;">Comentarios</button><form class="form_pedir_participar"><input type="hidden" value="${proposta.id}"><button type="submit" class="card-link btn btn-primary lato-bold solicitar_participar_butao" style="height: 100%; width: 100%;">Solicitar para participar</button></form></div></div></div>`}


let comentarios = function(comentarios, user) {
    conteudo = '';
    comentarios.forEach(function(comentario) {
        id_card_comentario = "id_card_comentario_" + comentario.id;
        conteudo += `<div class="card mx-auto mt-3 card_do_comentario" id="${id_card_comentario}"> <div class="card-body"> <h6 class="card-title lato-bold card_de_comentario_titulo fs-5"> <img class="comentario-foto" src="${comentario.user.foto_perfil}" alt="user"> ${comentario.dono_do_comentario} </h6> ${data_criacao(comentario)} <p class="card-text card_de_comentario_text lato-regular tamanho-padrao"> ${comentario.texto_comentario} </p> <div class="div-do-like"> <form class="form_likear_comentario"> <input type="hidden" name="comentario_id" value="${comentario.id}"> <button class="botao-likear-comentario btn" type="submit"> ${icone_likear(comentario, user)} </button> </form> </div> </div> </div>`
    });
    return conteudo;
}


let proposta_modal_card = function(id_modal_comentarios, proposta, user) {return `<div class="modal fade modal-lg" id="${id_modal_comentarios}" tabindex="-1" aria-hidden="true"> <div class="modal-dialog"><div class="modal-content"> <div class="modal-header"> <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button></div><div class="modal-body"> <form class="form_postar_comentario" novalidate> <div class="mb-2"> <input type="hidden" name="proposta_id" value="${proposta.id}"> <textarea class="form-control postar-comentario lato-regular fs-5" maxlength="1000" name="texto_comentario" placeholder="Comentário"></textarea> <span class="text-danger lato-bold postar_comentario_span fs-5" style="margin-top: 6px; margin-bottom: 5px;"></span></div> <button type="submit" class="botao-postar-comentario btn btn-info lato-bold fs-5" style="display: block; width: fit-content;">Comentar</button></form> <div class="mx-auto mt-3 comentarios_da_proposta">${comentarios(proposta.comentarios, user)}</div></div><div class="modal-footer"><button type="button"class="btn btn-secondary lato-bold"data-bs-dismiss="modal">Fechar</button></div></div></div></div>`;}


$(document).ready(function () {
    $('#input_de_ordenar').on("click", function () {
        ordenar = $('#recente').checked ? "recente" : "popular";

        jQuery.ajax({
            type: 'GET',
            url: `feed?ordenar=${ordenar}`,
            success: function (response) {
                propostas_feed_container = document.getElementById('propostas_feed_container');
                conteudo = ''
                response["propostas"].forEach(function(proposta) {
                    id_item_feed = "id_item_feed_" + proposta.id;
                    classe_background = "bg-" + proposta.tipo_proposta;
                    id_modal_comentarios = "modal_comentarios_" + proposta.id;

                    conteudo += proposta_card(proposta, response["user"], id_item_feed, classe_background, id_modal_comentarios);
                    conteudo += proposta_modal_card(id_modal_comentarios, proposta, response["user"])
                });
                propostas_feed_container.innerHTML = conteudo;
                carregar_event_listeners()
            }
        })
    });
});


function carregar_event_listeners() {
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
}


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