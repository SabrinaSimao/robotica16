# robotica16


Projeto Rob�tica 2017 - Sabrina S. + Jean W. + Hugo M.

--- Objetivo ---

O objetivo deste projeto � fazer um rob� (Neato) seguir um objeto enquanto implementa fun��es de sobreviv�ncia. Tal objeto pode ser ensinado previamente dentro do c�digo ou, para uma itera��o mais avan�ada, ser aprendido na hora pela pr�pria vis�o do rob�.
Foram feitos 2 v�deos do projeto, para melhor explicar o funcionamento do rob� e sua vis�o.

O primeiro v�deo, chamado Objeto Ensinado, mostra o rob� seguindo um objeto dado um certo inRange de cores, no qual o objeto pertence.

O segundo v�deo, chamado Objeto Aprendido, faz o rob� gravar uma foto do ambiente, e depois gravar uma segunda foto com um objeto na frente. Dessa forma, ele faz a subtra��o do objeto do fundo e "aprende" o que deve ser o objeto real. 

Em ambos v�deos voc� ver� o rob� seguindo seu alvo e desviando de obst�culos com seu laser, al�m de recuar e se afastar de objetos nos quais ele bater, a��o permitida pelos bumpers localizados na regi�o frontal.

--- Cria��o ---

O projeto em si foi feito ao longo das aulas e atendimentos fornecidos, al�m de certa parte ter sido elaborada em casa, nos fatidicos finais de semana! Uma certa divis�o de trabalho foi feita, o Hugo e a Sabrina come�aram trabalhando na parte de vis�o e filtro de imagem, estudando a camer� do rob� e tentando criar filtros e mascaras para o rob� enxergar. Enquanto isso, o Jean se dedicou a ver como o ROS (robot operational system) recebe as vari�veis importantes do Neato, como velocidade das rodas, rota��o, correr, parar etc. O importante � que at� o final do projeto, todos os membros do grupo estavam 100% integrados em ambos c�digos, sabendo como o rob� funcionava em todos os segmentos.

Dois arquivos foram elaborados para este projeto. O arquivo Follow.py, que implementa todos os filtros de imagem e define O QUE o rob� deve seguir. J� o arquivo localizar.py implementa COMO o rob� vai seguir tal objeto, a velocidade com que vai ir atras dele, e o que fazer quando o objeto sumir. Al�m disso, esse c�digo implementa as fun��es de sobreviv�ncia do rob�.
