import os
from flask import Flask, jsonify, request, send_from_directory
import F_auxiliares as fa
from BuscaNP import buscaNP
from BuscaP import buscaP

app = Flask(__name__, static_folder='.', static_url_path='')

MAP_FILES = {
    0: 'mapa.txt',
    1: 'mapa1.txt',
    2: 'mapa2.txt',
    3: 'mapa3.txt'
}

METHODS_NP = {
    'Amplitude / Busca em Largura': 'amplitude_grid',
    'Profundidade / Busca em Profundidade': 'profundidade_grid',
    'Profundidade Limitada': 'prof_limitada_grid',
    'Aprofundamento Iterativo': 'aprof_iterativo_grid',
    'Bidirecional': 'bidirecional_grid'
}

METHODS_P = {
    'Custo Uniforme': 'custo_uniforme_grid',
    'Greedy': 'greedy_grid',
    'A* (A-Estrela)': 'a_estrela_grid',
    'AIA* (A-Estrela Limitada)': 'aia_estrela_grid'
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
@app.route('/map/<int:mid>')
def get_map(mid):
    filename = MAP_FILES.get(mid)
    
    if not filename or not os.path.exists(filename):
        return jsonify({'error': 'map not found'}), 404
    mapa, nx, ny = fa.Gera_Problema_Grid_Fixo_P(filename)
    return jsonify({'mapa': mapa, 'nx': nx, 'ny': ny})
    

@app.route('/run', methods=['POST'])
def run_search():
    data = request.json or {}
    method_name = data.get('method')
    origem = data.get('origem')
    destino = data.get('destino')
    limite = data.get('limite')
    mapa_id = data.get('mapId', 0)

    if method_name not in METHODS_NP and method_name not in METHODS_P:
        return jsonify({'error': 'Método inválido'}), 400

    filename = MAP_FILES.get(mapa_id)
    print("======")
    print("mapa selecionado:", mapa_id)
    print("Arquivo:", filename)
    print("======")
    if not filename or not os.path.exists(filename):
        return jsonify({'error': 'map not found'}), 404

    mapa, nx, ny = fa.Gera_Problema_Grid_Fixo_P(filename)

    try:
        origem_coord = tuple(int(x) for x in origem.split(','))
        destino_coord = tuple(int(x) for x in destino.split(','))
    except Exception:
        return jsonify({'error': 'Origem ou destino inválido'}), 400

    if not (0 <= origem_coord[0] < nx and 0 <= origem_coord[1] < ny):
        return jsonify({'error': 'Origem fora do mapa'}), 400
    if not (0 <= destino_coord[0] < nx and 0 <= destino_coord[1] < ny):
        return jsonify({'error': 'Destino fora do mapa'}), 400
    if mapa[origem_coord[0]][origem_coord[1]] != 0 or mapa[destino_coord[0]][destino_coord[1]] != 0:
        return jsonify({'error': 'Origem ou destino não é célula livre'}), 400

    result = None
    try:
        if method_name in METHODS_NP:
            solver = buscaNP()
            method = getattr(solver, METHODS_NP[method_name], None)
            if method is None:
                raise AttributeError('Método não implementado')
            args = [origem_coord, destino_coord, nx, ny, mapa]
            if method_name == 'Profundidade Limitada':
                if not limite or limite <= 0:
                    return jsonify({'error': 'Limite inválido'}), 400
                args.append(int(limite))
            elif method_name == 'Aprofundamento Iterativo':
                if not limite or limite <= 0:
                    return jsonify({'error': 'Limite inválido'}), 400
                args.append(int(limite))
            result = method(*args)
        else:
            solver = buscaP()
            method = getattr(solver, METHODS_P[method_name], None)
            if method is None:
                raise AttributeError('Método não implementado')
            args = [origem_coord, destino_coord, mapa, nx, ny]
            result = method(*args);
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

    if not result:
        return jsonify({'method': method_name, 'origem': origem_coord, 'destino': destino_coord, 'custo': None, 'path': None, 'limite': limite})

    if isinstance(result, tuple) and len(result) == 2:
        caminho, custo = result
    elif isinstance(result, list):
        caminho = result
        custo = len(caminho) - 1 if caminho else None
    else:
        caminho = None
        custo = None

    if caminho is not None:
        caminho = [list(coord) if isinstance(coord, tuple) else coord for coord in caminho]

    return jsonify({
        'method': method_name,
        'origem': origem_coord,
        'destino': destino_coord,
        'custo': custo,
        'path': caminho,
        'limite': limite
    })

if __name__ == '__main__':
    app.run(debug=True)
