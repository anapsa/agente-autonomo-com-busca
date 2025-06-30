# Agente Autônomo com Busca

Este projeto é uma aplicação em Python que utiliza Pygame para visualizar algoritmos de busca em uma grade (grid) com terreno variado. O agente nasce em uma posição aleatória numa célula passável, enxerga um objeto como meta e executa um algoritmo de busca (BFS, DFS, UCS, Greedy, A*) para encontrar o caminho. Em seguida, ele se movimenta passo a passo, considerando o custo do terreno.

## Funcionalidades 


## Pré-requisitos 
* Python 3.8+
* Pygame
Caso não possua instalado, execute o seguinte comando

pip install pygame  

## Como visualizar 

1. Clone o repositório
    git clone https://github.com/anapsa/agente-autonomo-com-busca.git
2. Abra a pasta
   cd agente-autonomo-com-busca
3. Execute o programa com
   python3 main.py
4. Aperte 1 para visualizar a BFS, 2 para visualizar a DFS, 3 para visualizar custo uniforme, 4 para visualizar o algoritmo guloso e 5 para visualizar o A* 
