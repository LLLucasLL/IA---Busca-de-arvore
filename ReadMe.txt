INTRODUÇÃO

As buscas em árvores são estratégias utilizadas para encontrar um caminho entre um estado de origem e um estado de destino em um grafo ou grid. Cada estratégia define uma ordem diferente para expandir os nós da árvore de busca e, por isso, pode apresentar diferenças de custo, velocidade, uso de memória e garantia de encontrar uma solução.

Neste projeto, as buscas são divididas em dois grupos:

• Buscas não informadas (sem pesos): não utilizam conhecimento adicional sobre a distância até o objetivo. São adequadas para estudar a estrutura do espaço de estados ou para problemas em que não existe uma heurística disponível.

	- Busca em amplitude: explora os nós por níveis. É indicada quando se deseja encontrar um caminho com o menor número de passos, desde que todas as ações tenham o mesmo custo.
	- Busca em profundidade: explora um caminho até o fim antes de voltar e tentar outra alternativa. É útil quando a memória é limitada ou quando qualquer solução é suficiente, mas não garante o caminho mais curto.
	- Busca em profundidade limitada: é uma busca em profundidade com um limite máximo de níveis. Serve para evitar que a exploração avance indefinidamente.
	- Busca por aprofundamento iterativo: executa sucessivas buscas em profundidade limitada, aumentando o limite a cada tentativa. Combina o baixo uso de memória da profundidade com a capacidade da amplitude de encontrar uma solução mais rasa.
	- Busca bidirecional: realiza buscas simultaneamente a partir da origem e do destino até que elas se encontrem. É indicada quando é possível gerar sucessores nos dois sentidos e pode reduzir a quantidade de nós explorados.

• Buscas informadas (com pesos): utilizam custos das transições e, em alguns casos, uma heurística que estima a distância até o objetivo. São indicadas quando diferentes caminhos possuem custos diferentes ou quando se deseja direcionar a exploração para o destino.

	- Busca de custo uniforme: expande primeiro o caminho de menor custo acumulado. É apropriada para encontrar a solução de menor custo quando os custos das transições são não negativos.
	- Busca Greedy: prioriza o nó que parece estar mais próximo do objetivo segundo a heurística. Normalmente encontra soluções rapidamente, mas não garante o menor custo.
	- Busca A*: combina o custo já percorrido com uma estimativa do custo restante. Com uma heurística adequada, pode encontrar uma solução de menor custo explorando menos nós.
	- Busca AIA*: uma variação da busca A* que trabalha com limites de custo e aprofundamentos sucessivos. É útil para reduzir o uso de memória, mantendo a orientação da heurística.

As buscas sem pesos são executadas sobre grafos e grids sem custos diferenciados. As buscas com pesos consideram os custos associados às transições e exibem, além do caminho encontrado, o custo total da solução.

---------------------------------------------------------
REQUISITOS

• Python 3.14 (64 bits) ou superior
• NumPy
• Flask 2.3.2

---------------------------------------------------------
1. Verificar a versão do Python
---------------------------------------------------------

No Prompt de Comando ou PowerShell execute:

py --version

ou

python --version

---------------------------------------------------------
2. Instalar as dependências
---------------------------------------------------------

Instalar o NumPy:

py -m pip install numpy

Instalar o Flask:

py -m pip install Flask==2.3.2

Ou instalar todas as dependências utilizando o arquivo requirements.txt:

py -m pip install -r requirements.txt

---------------------------------------------------------
3. Caso ocorra erro com o Flask
---------------------------------------------------------

Atualize o Flask:

py -m pip install --upgrade flask

Verifique a versão instalada:

py -m pip show flask

A versão utilizada durante o desenvolvimento foi a 2.3.2.

---------------------------------------------------------
4. Executar o projeto
---------------------------------------------------------

Abra o terminal na pasta do projeto.

Exemplo:

cd C:\Users\Public\Documents\Projeto

Execute:

py api.py

ou

python api.py

Após iniciar o servidor, abra o navegador e acesse:

http://127.0.0.1:5000

---------------------------------------------------------
5. Funcionamento da Interface Gráfica
---------------------------------------------------------

A aplicação será aberta no navegador.

Na interface é possível:

• Selecionar um dos mapas disponíveis (Mapa 0 ao Mapa 3);
• Informar as coordenadas de Origem;
• Informar as coordenadas de Destino;
• Escolher o algoritmo de busca;
• Informar o limite quando o algoritmo exigir;
• Executar a busca;
• Limpar os resultados.

Após clicar em "Executar", o sistema:

• Carrega o mapa selecionado;
• Executa o algoritmo escolhido;
• Destaca o caminho encontrado no grid;
• Exibe o custo total da solução;
• Exibe o caminho percorrido na área "Resultado".

---------------------------------------------------------
6. Limpeza de Cache (caso necessário)
---------------------------------------------------------

Se ocorrer algum problema de cache durante a execução, execute:

pip cache purge

Remova os arquivos compilados do Python:

Windows PowerShell

Remove-Item -Recurse -Force __pycache__

Ou exclua manualmente todas as pastas __pycache__ do projeto.

Depois execute novamente:

python api.py

---------------------------------------------------------
Dependências do Projeto
---------------------------------------------------------

• Flask 2.3.2
• NumPy

Todas as dependências também estão disponíveis no arquivo requirements.txt.