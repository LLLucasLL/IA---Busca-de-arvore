// =============================================================================
// script.js — Interface de Busca em Grafos/Grids (Flask + HTML/JS)
// =============================================================================

const grid = document.getElementById('grid');

const metodoSelect = document.getElementById('metodo');
const limiteLabel = document.getElementById('label-limite');
const limiteInput = document.getElementById('limite');
const mapaSelect = document.getElementById('mapa');
const origemInputEl = document.getElementById('origem');
const destinoInputEl = document.getElementById('destino');
const resultadoEl = document.getElementById('textoResultado');

let origem = null;
let destino = null;
let mapaAtual = null;

// Métodos que exigem o campo "Limite". Precisa bater EXATAMENTE com o texto
// das <option> do <select id="metodo"> (é isso que methodSelect.value retorna
// quando a <option> não tem um atributo value= separado) e com o que a rota
// /run espera receber em "method" no backend.
const METODOS_COM_LIMITE = [
    'Profundidade Limitada',
    'Aprofundamento Iterativo'
];

function metodoPrecisaDeLimite(method) {
    return METODOS_COM_LIMITE.includes(method);
}

// Única função responsável por decidir se a caixa de limite aparece ou não.
// É chamada no evento "change" do select, ao limpar o formulário e uma vez
// no carregamento da página — assim a tela nunca fica com o campo escondido
// quando o método atual precisa dele (ex.: se o navegador restaurar a
// seleção do <select> ao recarregar a página, sem disparar "change").
function atualizarVisibilidadeLimite() {
    const method = metodoSelect.value.trim();
    if (metodoPrecisaDeLimite(method)) {
        limiteLabel.classList.remove('hidden');
        limiteInput.classList.remove('hidden');
    } else {
        limiteLabel.classList.add('hidden');
        limiteInput.classList.add('hidden');
        limiteInput.value = '';
    }
}

// Lê o campo de limite e valida que é um inteiro positivo.
// Retorna o número, ou null se estiver vazio/ inválido.
function lerLimiteValido() {
    const bruto = limiteInput.value.trim();
    if (!/^\d+$/.test(bruto)) return null;
    const valor = parseInt(bruto, 10);
    return valor > 0 ? valor : null;
}

function limparEstado() {
    origem = null;
    destino = null;
    origemInputEl.value = '';
    destinoInputEl.value = '';
    resultadoEl.innerText = 'Aguardando execução...';
    metodoSelect.value = 'Amplitude / Busca em Largura';
    atualizarVisibilidadeLimite();
    document.querySelectorAll('.celula').forEach((celula) => {
        celula.classList.remove('origem', 'destino', 'caminho');
    });
    if (mapaAtual) {
        renderMap(mapaAtual);
    }
}

async function loadMap(id) {

  console.log("Carregando mapa:", id);

    origem = null;
    destino = null;
    origemInputEl.value = '';
    destinoInputEl.value = '';

    const res = await fetch(`/map/${id}`);
    if (!res.ok) {
        alert('Erro ao carregar o mapa');
        return;
    }
    const data = await res.json();
    mapaAtual = data.mapa;
    renderMap(mapaAtual);
}

function renderMap(mapa) {
    grid.innerHTML = '';
    const linhas = mapa.length;
    const colunas = mapa[0].length;

    grid.style.gridTemplateColumns = `repeat(${colunas}, 70px)`;
    grid.style.gridTemplateRows = `repeat(${linhas}, 70px)`;

    for (let i = 0; i < linhas; i++) {
        for (let j = 0; j < colunas; j++) {
            const celula = document.createElement('div');
            celula.className = 'celula';
            celula.dataset.x = i;
            celula.dataset.y = j;

            if (mapa[i][j] !== 0) celula.classList.add('obstaculo');

            celula.onclick = () => clicou(celula);
            grid.appendChild(celula);
        }
    }
}

function clicou(c) {
    if (c.classList.contains('obstaculo')) return;

    if (!origem) {
        origem = c;
        c.classList.add('origem');
        origemInputEl.value = `${c.dataset.x},${c.dataset.y}`;
        return;
    }

    if (!destino && c !== origem) {
        destino = c;
        c.classList.add('destino');
        destinoInputEl.value = `${c.dataset.x},${c.dataset.y}`;
    }
}

function lerCoordenadasDoInput(id) {
    const valor = document.getElementById(id).value.trim();
    if (!valor) return null;
    const partes = valor.split(',').map((p) => parseInt(p.trim(), 10));
    return partes.length === 2 && !partes.some(Number.isNaN) ? partes : null;
}

function clearPathHighlights() {
    document.querySelectorAll('.celula.caminho').forEach((celula) => celula.classList.remove('caminho'));
}

function highlightPath(path) {
    clearPathHighlights();
    path.forEach((coord) => {
        const selector = `.celula[data-x='${coord[0]}'][data-y='${coord[1]}']`;
        const cell = document.querySelector(selector);
        if (cell && !cell.classList.contains('origem') && !cell.classList.contains('destino')) {
            cell.classList.add('caminho');
        }
    });
}

// -----------------------------------------------------------------------
// EVENTOS
// -----------------------------------------------------------------------

metodoSelect.addEventListener('change', atualizarVisibilidadeLimite);

mapaSelect.addEventListener('change', (e) => {
    loadMap(e.target.selectedIndex);
});

document.getElementById('limpar').onclick = limparEstado;

document.getElementById('executar').onclick = async () => {
    const origemInput = lerCoordenadasDoInput('origem');
    const destinoInput = lerCoordenadasDoInput('destino');

    if (!origemInput || !destinoInput) {
        alert('Informe origem e destino válidos no formato x,y.');
        return;
    }

    const method = metodoSelect.value.trim();
    const precisaDeLimite = metodoPrecisaDeLimite(method);
    const limitValue = lerLimiteValido();

    if (precisaDeLimite && limitValue === null) {
        alert('Informe um limite válido (número inteiro maior que zero).');
        limiteInput.focus();
        return;
    }

    const payload = {
        method,
        origem: `${origemInput[0]},${origemInput[1]}`,
        destino: `${destinoInput[0]},${destinoInput[1]}`,
        mapId: mapaSelect.selectedIndex,
        limite: precisaDeLimite ? limitValue : null
    };

    resultadoEl.innerText = 'Executando algoritmo...';

    try {
        const res = await fetch('/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const json = await res.json();

        if (!res.ok) {
            resultadoEl.innerHTML = `Erro: ${json.error || 'Falha na execução'}`;
            return;
        }

        const origemTexto = Array.isArray(json.origem) ? json.origem.join(',') : String(json.origem || '');
        const destinoTexto = Array.isArray(json.destino) ? json.destino.join(',') : String(json.destino || '');

        if (!json.path || !Array.isArray(json.path) || json.path.length === 0) {
            resultadoEl.innerHTML = `Método: ${json.method || method}<br><br>Origem: (${origemTexto})<br>Destino: (${destinoTexto})<br><br>Nenhum caminho encontrado.`;
            clearPathHighlights();
            return;
        }

        resultadoEl.innerHTML = `Método: ${json.method || method}<br><br>Origem: (${origemTexto})<br>Destino: (${destinoTexto})<br>Custo: ${json.custo ?? 'N/A'}<br>Limite: ${json.limite ?? 'N/A'}<br><br>Caminho: ${json.path.map((p) => `(${p[0]},${p[1]})`).join(' → ')}`;
        highlightPath(json.path);
    } catch (error) {
        resultadoEl.innerHTML = `Erro: ${error.message || 'Falha na comunicação com o servidor'}`;
    }
};

// Estado inicial: sincroniza a caixa de limite com o método já selecionado
// no HTML (cobre o caso do navegador restaurar a seleção do <select> ao
// recarregar a página) e carrega o primeiro mapa da lista.
atualizarVisibilidadeLimite();
loadMap(0);