# ai-sokoban-solver

Implementation of common algorithms for solving a simplified sokoban game.

## TODO Code

- [x] Change box emoji to numbered squares
- [ ] Add command to generate a random map

## TODO Docs

1. README.md

- [ ] Engenharia de Software: Documentar a estrutura do Estado (frozenset) e justificar que foi feito assim para otimizar o hash no mapa de visitados O(1).
- [ ] A Matemática da Busca: Explicar explicitamente a Função Sucessora, Objetivo e Custo.
- [ ] A Prova de Admissibilidade: Escrever o parágrafo cravando que a Heurística relaxa o problema (ignora paredes e tempo de transição sem carga), logo o custo calculado teoricamente é sempre menor ou igual ao labirinto real, garantindo o caminho ótimo.
- [ ] O Estudo de Escalabilidade: Rodar o código nos 4 cenários (8x8, 16x16, 24x24, 64x64). Fazer uma tabela cruzando Tamanho do Mapa vs Quantidade de Estados Visitados e Tempo de Execução de cada um dos 3 algoritmos. (O Dijkstra vai sangrar aqui, registre isso em números).

2. Slides

- [ ] Slide 1-2 (Modelagem): Mostrar visualmente o que é um Estado (a foto do tabuleiro) e quais são as transições válidas (andar vs carregar).
- [ ] Slide 3 (Mecânica): Mostrar o teste de objetivo (conjunto de caixas zerado).
- [ ] Slide 4-5 (Matemática): Colocar a fórmula algébrica da Função Custo g(n) e da Função Heurística Composta h(n) na tela. Sem código. Explicar como a multiplicação pelo peso afasta o A* de caminhos burros.
- [ ] Slide 6 (Comparativo Visual): Pegar um labirinto minúsculo resolvido. Mostrar os passos e o Custo Final encontrado pelo Dijkstra, Guloso e A*.
- [ ] Slide 7 (O Veredito): Interpretação final. Explicar por que o Ganancioso erra a otimização de custo (é apressado), por que o Dijkstra é insano no uso de memória (é cego) e por que o A* é a ferramenta definitiva.
