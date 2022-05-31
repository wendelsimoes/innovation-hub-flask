$(document).ready(function () {
    $('.anchor-like-comentario').on("click", function () {
        icone_do_like = $(this).children('i')[0];
        if (icone_do_like.classList.contains('bi-hand-thumbs-up-fill')) {
            icone_do_like.classList.remove('bi-hand-thumbs-up-fill');
            icone_do_like.classList.add('bi-hand-thumbs-up');
        } else {
            icone_do_like.classList.remove('bi-hand-thumbs-up');
            icone_do_like.classList.add('bi-hand-thumbs-up-fill');
        }
    })
});

function carregar_comentarios(comentarios, id_modal_comentarios) {
    div_comentarios = $(`#${id_modal_comentarios} .comentarios_da_proposta`);
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
            class: "card-text card_de_comentario_text",
        });

        card_de_comentario_text.append(comentario["texto_comentario"]);
        card_de_comentario_titulo.append(comentario["dono_do_comentario"]);
        card_de_comentario_body.append(card_de_comentario_titulo);
        card_de_comentario_body.append(card_de_comentario_subtitulo);
        card_de_comentario_body.append(card_de_comentario_text);
        card_de_comentario.append(card_de_comentario_body);
        div_comentarios.append(card_de_comentario);

        var div_do_like = $("<div>", { class: "div-do-like" });

        var botao_do_like = $("<a>", { class: "anchor-like-comentario" });


        var classe_do_link = comentario["likeado"] ? "bi bi-hand-thumbs-up-fill botao-like-comentario" : "bi bi-hand-thumbs-up botao-like-comentario";

        var icone_do_like = $("<i>", { class: classe_do_link });

        botao_do_like.on("click", function () {
            likear_comentario(comentario["id"]);
            icone_do_like.toggleClass('bi-hand-thumbs-up-fill bi-hand-thumbs-up');
        });

        botao_do_like.append(icone_do_like);
        div_do_like.append(botao_do_like);
        card_de_comentario_body.append(div_do_like);
    });
}

function enviar_comentario(id_proposta, id_modal_comentarios) {
    texto_comentario = $(`#${id_modal_comentarios} .postar-comentario`).val();

    $(function () {
        $.post(
            'comentar',
            {
                texto_comentario: texto_comentario,
                id_proposta: id_proposta,
            },
            function (response) {
                if (response["status"] == 400) {
                    $(`#${id_modal_comentarios} .postar_comentario_span`).text(
                        response["mensagem"]
                    );
                    return;
                }

                $(`#${id_modal_comentarios} .postar_comentario_span`).text("");
                $(`#${id_modal_comentarios} .postar-comentario`).val("");

                carregar_comentarios(response, id_modal_comentarios);
            }
        );
    });
}

function likear_comentario(id_comentario) {
    $(function () {
        $.post(
            'likear_comentario',
            {
                id_comentario: id_comentario
            },
            function (response) {
            });
    });
}

function likear_proposta(id_proposta, id_item_feed) {
    $(function () {
        $.post(
            'likear_proposta',
            {
                id_proposta: id_proposta
            },
            function (response) {
                icone = $(`#${id_item_feed} .botao-like-proposta`).toggleClass('bi-hand-thumbs-up-fill bi-hand-thumbs-up');
            });
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