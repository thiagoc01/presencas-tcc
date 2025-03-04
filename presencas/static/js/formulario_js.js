VARIAVEL_MAX = {
    'links' : 8,
    'imagens': 12,
    'palavras_chave' : 12,
    'linguagem' : 12,
    'cidade_atuacao' : 4,
    'estado_atuacao' : 4,
    'pais_atuacao' : 4
};
id_intervalo = undefined;
id_solicitacao = Math.floor(Math.random() * (1e20 - 1) + 1).toString();

function remove_ultimo_campo(evento)
{
    const [nome, variavel, nome_botao_adicionar] =
            [evento.target.name, evento.data.variavel, evento.data.nome_botao_adicionar];
            
    $(`#${variavel} > tbody > tr `).filter( (_, elemento) => {
        if ($(elemento).find(`[name*="${nome}"]`).length > 0)
            return elemento;
    }).remove();
    if ($(`#${variavel} > tbody`).children().length == VARIAVEL_MAX[variavel] - 1)
        $(`#${nome_botao_adicionar}`).prop('disabled', false);
}

function adiciona_bloco(evento)
{
    const [variavel, nome_botao_remover, nome_botao_adicionar, callback] =
        [evento.data.variavel, evento.data.nome_botao_remover, evento.data.nome_botao_adicionar, evento.data.callback];
    if ($(`#${variavel} > tbody`).children().length == 0)
    {
        let template_URL;

        switch (variavel) {
            case 'links':
                template_URL = $($.parseHTML(A)).find(':nth-child(1)');
                break;

            case 'imagens':
                template_URL = $($.parseHTML(B)).find(':nth-child(1)');
                break;

            case 'palavras_chave':
                template_URL = $($.parseHTML(C)).find(':nth-child(1)');
                break;

            case 'linguagem':
                template_URL = $($.parseHTML(D)).find(':nth-child(1)');
                break;

            case 'cidade_atuacao':
                template_URL = $($.parseHTML(E)).find(':nth-child(1)');
                break;

            case 'estado_atuacao':
                template_URL = $($.parseHTML(F)).find(':nth-child(1)');
                break;

            case 'pais_atuacao':
                template_URL = $($.parseHTML(G)).find(':nth-child(1)');
                break;
        }

        $(template_URL).children('[id *= -erro-]').remove();
        template_URL = $(template_URL).find(":nth-child(1)").get(0).outerHTML;
        $(`#${variavel} > tbody`).append(template_URL.replaceAll(new RegExp(`${variavel}-[0-9]+`, 'g'), variavel + '-' + 0));
        $(`#${variavel} tbody tr [name*="-${nome_botao_remover}"]:last`).on("click", evento.data, callback);
        return;
    }

    let ultimo_id_campo = String($(`#${variavel} > tbody > tr:last > td > fieldset`).attr('name'));
    let [label_for_anterior, novo_id] = [ultimo_id_campo.split('-')[0], Number(ultimo_id_campo.split('-')[1]) + 1];
    let novo_campo = $(`#${variavel} > tbody > tr:last`).clone();
    $(novo_campo).find("[id *= -erro-]").remove();
    $(novo_campo).html($(novo_campo).html().replaceAll(new RegExp(`${label_for_anterior}-[0-9]+`, 'g'), label_for_anterior + '-' + novo_id));
    $(`#${variavel}`).append($(novo_campo).prop('outerHTML'));
    $(`#${variavel} tbody tr [name*="-${nome_botao_remover}"]:last`).on("click", evento.data, callback);
    if (variavel == 'imagens')
        $("#imagens tbody tr input[type='file']:last").prev().css('background-color', '').css('color', '')
    if ($(`#${variavel} > tbody`).children().length == VARIAVEL_MAX[variavel])
        $(`#${nome_botao_adicionar}`).prop('disabled', true);
}

$('#adicionar_campo_link').on('click', {variavel : 'links', nome_botao_remover : 'remover_campo_link',
                    nome_botao_adicionar : 'adicionar_campo_link', callback: remove_ultimo_campo}, adiciona_bloco);

$('#adicionar_campo_imagem').on('click', {variavel : 'imagens', nome_botao_remover : 'remover_campo_imagem',
    nome_botao_adicionar : 'adicionar_campo_imagem', callback: remove_ultimo_campo}, adiciona_bloco);

$('#adicionar_campo_palavras_chave').on('click', {variavel : 'palavras_chave', nome_botao_remover : 'remover_campo_palavras_chave',
    nome_botao_adicionar : 'adicionar_campo_palavras_chave', callback: remove_ultimo_campo}, adiciona_bloco);

$('#adicionar_campo_linguagem').on('click', {variavel : 'linguagem', nome_botao_remover : 'remover_campo_linguagem',
    nome_botao_adicionar : 'adicionar_campo_linguagem', callback: remove_ultimo_campo}, adiciona_bloco);

$('#adicionar_campo_cidade_atuacao').on('click', {variavel : 'cidade_atuacao', nome_botao_remover : 'remover_campo_cidade_atuacao',
    nome_botao_adicionar : 'adicionar_campo_cidade_atuacao', callback: remove_ultimo_campo}, adiciona_bloco);

$('#adicionar_campo_estado_atuacao').on('click', {variavel : 'estado_atuacao', nome_botao_remover : 'remover_campo_estado_atuacao',
    nome_botao_adicionar : 'adicionar_campo_estado_atuacao', callback: remove_ultimo_campo}, adiciona_bloco);

$('#adicionar_campo_pais_atuacao').on('click', {variavel : 'pais_atuacao', nome_botao_remover : 'remover_campo_pais_atuacao',
    nome_botao_adicionar : 'adicionar_campo_pais_atuacao', callback: remove_ultimo_campo}, adiciona_bloco);

$('#links [name*="-remover_campo_link"]').on("click", {variavel: 'links', nome_botao_adicionar : 'adicionar_campo_link'}, remove_ultimo_campo);

$('#imagens [name*="-remover_campo_imagem"]').on("click", {variavel: 'imagens', nome_botao_adicionar : 'adicionar_campo_imagem'}, remove_ultimo_campo);

$('#palavras_chave [name*="-remover_campo_palavras_chave"]').on("click", {variavel: 'palavras_chave', nome_botao_adicionar : 'adicionar_campo_palavras_chave'}, remove_ultimo_campo);

$('#linguagem [name*="-remover_campo_linguagem"]').on("click", {variavel: 'linguagem', nome_botao_adicionar : 'adicionar_campo_linguagem'}, remove_ultimo_campo);

$('#cidade_atuacao [name*="-remover_campo_cidade_atuacao"]').on("click", {variavel: 'cidade_atuacao', nome_botao_adicionar : 'adicionar_campo_cidade_atuacao'}, remove_ultimo_campo);

$('#estado_atuacao [name*="-remover_campo_estado_atuacao"]').on("click", {variavel: 'estado_atuacao', nome_botao_adicionar : 'adicionar_campo_estado_atuacao'}, remove_ultimo_campo);

$('#pais_atuacao [name*="-remover_campo_pais_atuacao"]').on("click", {variavel: 'pais_atuacao', nome_botao_adicionar : 'adicionar_campo_pais_atuacao'}, remove_ultimo_campo);

$(':root').on("change", 'input[type="file"]', function (e) {
    const arquivos = e.target.files;
    for (let i = 0 ; i < arquivos.length ; i++)
    {
        if (arquivos[i].name.search(/(.png|.jpeg|.jpg|.jfif)$/g) == -1)
            $(`input[name="${e.target.name}"]`).val('');

        if ($(`input[name="${e.target.name}"]`).val())
            $(`input[name="${e.target.name}"]`).prev().css('background-color', 'green').css('color', 'white')
        else
            $(`input[name="${e.target.name}"]`).prev().css('background-color', '').css('color', "")
    }
});

['nome', 'trajetoria', 'producao', 'ultima_atualizacao', 'pesquisante',
    'email_pesquisante', 'data_inicio', 'data_fim', 'quantidade', 'genero', 'pagina', 'cidade', 'estado'].forEach(campo => {
    $(`#${campo}`).on("input", function (evento) {
        $('#' + campo + '-erro').remove();
        $(evento.target).off("input");
    });
});

['links', 'imagens', 'palavras_chave', 'linguagem', 'cidade_atuacao', 'estado_atuacao', 'pais_atuacao'].forEach(campo => {
    $(`#${campo} td input`).on("input", function (evento) {
        $(evento.target).parent($(`#${evento.target.id}`)).next('[id *= -erro-]').remove();
        $(evento.target).off("input");
    });
});

function obtem_progresso(ID)
{
    $.ajax({
        url: `/api/obter_progresso/${ID}`,
        type: "GET",

        dataType: 'text',

        processData: false,

        contentType: false,

        success: data => {
            porcentagem = (data * 100).toFixed(2);
            $("#barra-carregamento").css('width', porcentagem + '%');
            $("#barra-carregamento").text(Math.round(porcentagem) + '%');
            $("#barra-carregamento").attr('aria-valuenow', porcentagem);

            if (Math.round(porcentagem) == 100)
                clearInterval(id_intervalo);     // Se chegar em 100%, cancela novos requests antes de success do submit cancelar
        }
    });
}

$("form").submit(function(e){
    e.preventDefault();

    $.ajax({
        type: "POST",

        contentType: false,

        data: new FormData(this),

        dataType: 'html',

        processData: false,

        beforeSend: function() {
            $("body").prepend($.parseHTML(HTML_BARRA_PROGRESSO));
            $("body").css('scrollbar-width', '100vh');
            id_intervalo = setInterval(obtem_progresso, 500, id_solicitacao);
            this.data.append('id_solicitacao', id_solicitacao);
        },

        success: data => {
            clearInterval(id_intervalo);
            document.open();
            document.write(data);
            document.close();
        },

        error: data => {
            clearInterval(id_intervalo);
            document.write(data.responseText);
            document.close();
        }
    });
});