const REGEX_SIMBOLOS = /[@_!#$%^&*()<>?\/\|}{~:\.]/g;
const REGEX_MINUSCULA = /[a-z]/g;
const REGEX_MAIUSCULA = /[A-Z]/g;
const REGEX_NUMERO = /[0-9]/g;

function altera_propriedades(verificacao, div, classe)
{
    let cor, adicionar, remover;

    if (verificacao)
        cor = 'green', adicionar = 'fa-check', remover = 'fa-xmark';
        
    else
        cor = 'red', adicionar = 'fa-xmark', remover = 'fa-check';

    if (!div.find(classe + ' i').hasClass(adicionar))
        div.find(classe + ' i').addClass(adicionar).css('color', cor).removeClass(remover);
}

function verifica_minimalidade_senha()
{
    const SENHA = $('#senha').val();
    const MINIMOS_SENHA = SENHA.length >= 10 && SENHA.match(REGEX_MAIUSCULA)
                    && SENHA.match(REGEX_MINUSCULA) && SENHA.match(REGEX_NUMERO) && SENHA.match(REGEX_SIMBOLOS);

    if (SENHA == $('#confirmar_senha').val() && MINIMOS_SENHA)
        $('#botao-cadastrar').prop('disabled', false);

    else
        $('#botao-cadastrar').prop('disabled', true);
}

function verifica_condicoes(e)
{
    const SENHA = e.target.value;
    const div_verificador_senha = $('#verificador-minimalidade-senha');

    altera_propriedades(SENHA.length >= 10, div_verificador_senha, '.verificador-10-caracteres');
    altera_propriedades(SENHA.match(REGEX_MAIUSCULA) && SENHA.match(REGEX_MINUSCULA), div_verificador_senha, '.verificador-letras');
    altera_propriedades(SENHA.match(REGEX_NUMERO), div_verificador_senha, '.verificador-numero');
    altera_propriedades(SENHA.match(REGEX_SIMBOLOS), div_verificador_senha, '.verificador-caractere-especial');

    verifica_minimalidade_senha();
}

function apaga_erro(e)
{
        $('#' + e.data.campo + '-erro').remove();
        $(e.target).off("input", apaga_erro);
}

$('#senha').on('input', verifica_condicoes);
$('#confirmar_senha').on('input', verifica_minimalidade_senha);

['senha', 'confimar_senha'].forEach(campo => {
    $(`#${campo}`).on("input", {campo: campo}, apaga_erro);
});