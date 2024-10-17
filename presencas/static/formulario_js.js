const MAX_LINKS = 8;
const MAX_IMAGENS = MAX_PALAVRAS_CHAVE = 12;

function remove_ultimo_campo(evento)
{
    const [nome, variavel, nome_botao_adicionar] =
            [evento.target.name, evento.data.variavel, evento.data.nome_botao_adicionar];
            
    $(`#${variavel} > tbody > tr `).filter( (_, elemento) => {
        if ($(elemento).find(`[name*="${nome}"]`).length > 0)
            return elemento;
    }).remove();
    if ($(`#${variavel} > tbody`).children().length == (variavel == 'links' ? MAX_LINKS - 1 :
            variavel == 'imagens' ? MAX_IMAGENS - 1 : MAX_PALAVRAS_CHAVE - 1))
        $(`#${nome_botao_adicionar}`).prop('disabled', false);
}

function adiciona_bloco(evento)
{
    const [variavel, nome_botao_remover, nome_botao_adicionar, callback] =
        [evento.data.variavel, evento.data.nome_botao_remover, evento.data.nome_botao_adicionar, evento.data.callback];
    if ($(`#${variavel} > tbody`).children().length == 0)
    {
        let template_URL;
        if (variavel == 'links')
            template_URL = $($.parseHTML(A)).find(':nth-child(1)');
        else if (variavel == 'imagens')
            template_URL = $($.parseHTML(B)).find(':nth-child(1)');
        else
            template_URL = $($.parseHTML(C)).find(':nth-child(1)');
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
    if ($(`#${variavel} > tbody`).children().length == (variavel == 'links' ?  MAX_LINKS : variavel == 'imagens' ? MAX_IMAGENS : MAX_PALAVRAS_CHAVE))
        $(`#${nome_botao_adicionar}`).prop('disabled', true);
}

$('#adicionar_campo_link').on('click', {variavel : 'links', nome_botao_remover : 'remover_campo_link',
                    nome_botao_adicionar : 'adicionar_campo_link', callback: remove_ultimo_campo}, adiciona_bloco);

$('#adicionar_campo_imagem').on('click', {variavel : 'imagens', nome_botao_remover : 'remover_campo_imagem',
    nome_botao_adicionar : 'adicionar_campo_imagem', callback: remove_ultimo_campo}, adiciona_bloco);

$('#adicionar_campo_palavras_chave').on('click', {variavel : 'palavras_chave', nome_botao_remover : 'remover_campo_palavras_chave',
    nome_botao_adicionar : 'adicionar_campo_palavras_chave', callback: remove_ultimo_campo}, adiciona_bloco);

$('#links [name*="-remover_campo_link"]').on("click", {variavel: 'links', nome_botao_adicionar : 'adicionar_campo_link'}, remove_ultimo_campo);

$('#imagens [name*="-remover_campo_imagem"]').on("click", {variavel: 'imagens', nome_botao_adicionar : 'adicionar_campo_imagem'}, remove_ultimo_campo);

$('#palavras_chave [name*="-remover_campo_palavras_chave"]').on("click", {variavel: 'palavras_chave', nome_botao_adicionar : 'adicionar_campo_palavras_chave'}, remove_ultimo_campo);

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
    'email_pesquisante', 'data_nascimento', 'genero', 'pagina'].forEach(campo => {
    $(`#${campo}`).on("input", function (evento) {
        $('#' + campo + '-erro').remove();
        $(evento.target).off("input");
    });
});

['links', 'imagens', 'palavras_chave'].forEach(campo => {
    $(`#${campo} td input`).on("input", function (evento) {
        $(evento.target).parent($(`#${evento.target.id}`)).next('[id *= -erro-]').remove();
        $(evento.target).off("input");
    });
});