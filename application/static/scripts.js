$(document).ready(function () {
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
                    let codigo = JSON.parse(response)["status"];
    
                    if (codigo == 400) {
                        let liveToast = $('.toast-erro');
                        liveToast.find('.toast-body').text(JSON.parse(response)["mensagem"]);
                        let toast = new bootstrap.Toast(liveToast);
                        
                        toast.show();
                        return
                    }
    
                    if (codigo == 200) {
                        let liveToast = $('.toast-sucesso');
                        liveToast.find('.toast-body').text(JSON.parse(response)["mensagem"]);
                        let toast = new bootstrap.Toast(liveToast);
                        
                        toast.show();
                        return
                    }
                });
        });
    });

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
                    novo_icone = null
                    if (JSON.parse(response)["favoritado"]) {
                        botao_do_favorito.text("");
                        novo_icone = $("<i>", {
                            class:
                                "bi-star-fill"
                        });
                    } else {
                        botao_do_favorito.text("");
                        novo_icone = $("<i>", {
                            class:
                                "bi-star"
                        });
                    }

                    texto = document.createTextNode(" " + JSON.parse(response)["mensagem"] + " ");
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

        card_de_comentario_text.append(comentario["texto_comentario"]);
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

        texto = document.createTextNode(" " + comentario["numeros_de_like"] + " ");
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

                var $list = $("<li>", { id: "foo", "class": classe_aleatoria });
                $list.append(response["mensagem"]);
                $('#lista_de_membros').append($list);

                $('#div_invisivel_membros').text("");
                membros.forEach(element => {
                    $('<input>').attr({
                        type: 'hidden',
                        name: 'membros',
                        value: element
                    }).appendTo('#div_invisivel_membros');
                });
            }
        })
    });
});

function exibir_notificacoes() {
    mostrar = "dropdown-menu notification-ui_dd show";
    esconder = "dropdown-menu notification-ui_dd hide";

    notifications = document.querySelector('.notification-ui_dd');
    console.log(notifications);

    if (notifications.className == mostrar) {
        notifications.className = esconder;
    } else {
        notifications.className = mostrar;
    }
}