# Como executar

## Etapa 1-2
As etapas 1 e 2 do projeto são executados no mesmo programa python.
### Entrada
Dentro da pasta Etapa1-2, coloque as imagens de entrada na pasta Entrada, e execute o comando. A ordem em que as imagens ficam na pasta de entrada altera o resultado do processo, o melhor resultado é obtido quando as imagens são colocadas da perspectiva mais a direita para a mais a esquerda, considerando uma ordenação crescente pelos nomes das imagens.
```python etapa1-2.py```
### Saída
A imagem de saída que será utilizada nas próximas etapas é gerada na pasta Saida com o nome imagem_composta.jpg, as demais imagens geradas são partes do processo feito nessa etapa.

## Etapa 3
### Entrada
Dentro da pasta Etapa3, coloque a imagem de saída da etapa 1-2 na pasta Entrada, e execute o comando.
```python etapa3.py --encoder vitl --img-path "\Entrada" --outdir "\Saida"```
### Saída
O arquivo de saída, com a nuvem de pontos, que será utilizada na próxima etapa é gerado na pasta Saida com o nome de resultado_depth.txt.

## Etapa 4
### Entrada
Dentro da pasta Etapa4, coloque a imagem de saída da etapa 1-2 e o arquivo gerado na etapa 3 na pasta Entrada, e execute o comando.
```python etapa4.py```
### Saída
A visualização da malha final é gerada e mostrada durante a execução do programa.