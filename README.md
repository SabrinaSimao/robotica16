
# Projeto Rob�tica 2017 - Sabrina S. + Jean W. + Hugo M.

--- Objetivo ---

O objetivo deste projeto � fazer um rob� (Neato) seguir um objeto enquanto implementa fun��es de sobreviv�ncia. Tal objeto pode ser ensinado previamente dentro do c�digo ou, para uma itera��o mais avan�ada, ser aprendido na hora pela pr�pria vis�o do rob�.
Foram feitos v�rios v�deos do projeto, para melhor explicar o funcionamento do rob� e sua vis�o.

Alguns dos v�deos cobrem o c�digo rodando por completo, com o rob� seguindo, desviando, parando e evitando perigos tudo ao mesmo tempo.

Outros v�deos cobrem as funcionalidades separado, para melhor perceber como foram aplicadas. Pode-se ver a demonstra��o do laser evitando obst�culos, do c�digo criando uma back projection e fazendo filtros, e do sistema de seguir, parar e procurar.


--- Cria��o ---

O projeto em si foi feito ao longo das aulas e atendimentos fornecidos, al�m de certa parte ter sido elaborada em casa, nos fatidicos finais de semana! Uma certa divis�o de trabalho foi feita, o Hugo e a Sabrina come�aram trabalhando na parte de vis�o e filtro de imagem, estudando a camer� do rob� e tentando criar filtros e mascaras para o rob� enxergar. Enquanto isso, o Jean se dedicou a ver como o ROS (robot operational system) recebe as vari�veis importantes do Neato, como velocidade das rodas, rota��o, correr, parar etc. Isso tudo nas primeiras aulas do projeto, pois ao longo dele as tarefas foram se ramificando e todos come�aram a trabalhar mais uniformemente. O fundamental � que at� o final do projeto, todos os membros do grupo estavam 100% integrados em ambos c�digos, sabendo como o rob� funcionava em todos os segmentos.

Dois arquivos foram elaborados para este projeto. O arquivo Follow.py, que implementa todos os filtros de imagem e define O QUE o rob� deve seguir. J� o arquivo localizar.py implementa COMO o rob� vai seguir tal objeto, a velocidade com que vai ir atras dele, e o que fazer quando o objeto sumir. Al�m disso, esse c�digo implementa as fun��es de sobreviv�ncia do rob� (laser e bumper).
