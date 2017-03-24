
# Projeto Robótica 2017 - Sabrina S. + Jean W. + Hugo M.

--- Objetivo ---

O objetivo deste projeto é fazer um robô (Neato) seguir um objeto enquanto implementa funções de sobrevivência. Tal objeto pode ser ensinado previamente dentro do código ou, para uma iteração mais avançada, ser aprendido na hora pela própria visão do robô.
Foram feitos vários vídeos do projeto, para melhor explicar o funcionamento do robô e sua visão.

Alguns dos vídeos cobrem o código rodando por completo, com o robô seguindo, desviando, parando e evitando perigos tudo ao mesmo tempo.

Outros vídeos cobrem as funcionalidades separado, para melhor perceber como foram aplicadas. Pode-se ver a demonstração do laser evitando obstáculos, do código criando uma back projection e fazendo filtros, e do sistema de seguir, parar e procurar.


--- Criação ---

O projeto em si foi feito ao longo das aulas e atendimentos fornecidos, além de certa parte ter sido elaborada em casa, nos fatidicos finais de semana! Uma certa divisão de trabalho foi feita, o Hugo e a Sabrina começaram trabalhando na parte de visão e filtro de imagem, estudando a camerâ do robô e tentando criar filtros e mascaras para o robô enxergar. Enquanto isso, o Jean se dedicou a ver como o ROS (robot operational system) recebe as variáveis importantes do Neato, como velocidade das rodas, rotação, correr, parar etc. Isso tudo nas primeiras aulas do projeto, pois ao longo dele as tarefas foram se ramificando e todos começaram a trabalhar mais uniformemente. O fundamental é que até o final do projeto, todos os membros do grupo estavam 100% integrados em ambos códigos, sabendo como o robô funcionava em todos os segmentos.

Dois arquivos foram elaborados para este projeto. O arquivo Follow.py, que implementa todos os filtros de imagem e define O QUE o robô deve seguir. Já o arquivo localizar.py implementa COMO o robô vai seguir tal objeto, a velocidade com que vai ir atras dele, e o que fazer quando o objeto sumir. Além disso, esse código implementa as funções de sobrevivência do robô (laser e bumper).
