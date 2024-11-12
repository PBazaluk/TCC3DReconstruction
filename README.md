# Como executar

## Etapa 2-3
As etapas 2 e 3 do projeto são executados no mesmo programa python.
### Entrada
Dentro da pasta Etapa2-3, coloque as imagens de entrada na pasta Entrada, e execute o comando
```python etapa2-3.py```
### Saída
A imagem de saída que será utilizada nas próximas etapas é gerada na pasta Saida

## Etapa 4
### Entrada
Dentro da pasta Etapa4, coloque a imagem de saída da etapa 2-3 na pasta Entrada, e execute o comando
```python etapa4.py --encoder vitl --img-path "\Entrada" --outdir "\Saida"```
### Saída
O arquivo de saída, com a nuvem de pontos, que será utilizada na próxima etapa é gerado na pasta Saida

## Etapa 5
### Entrada
Dentro da pasta Etapa5, coloque a imagem de saída da etapa 2-3 e o arquivo gerado na etapa 4 na pasta Entrada, e execute o comando
```python etapa5.py```
### Saída
A visualização da malha final é gerada e mostrada durante a execução do programa