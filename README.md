# robotica16


Projeto Robótica 2017 - Sabrina S. + Jean W. + Hugo M.

--- Objetivo ---

O objetivo deste projeto é fazer um robô (Neato) seguir um objeto enquanto implementa funções de sobrevivência. Tal objeto pode ser ensinado previamente dentro do código ou, para uma iteração mais avançada, ser aprendido na hora pela própria visão do robô.
Foram feitos 2 vídeos do projeto, para melhor explicar o funcionamento do robô e sua visão.

O primeiro vídeo, chamado Objeto Ensinado, mostra o robô seguindo um objeto dado um certo inRange de cores, no qual o objeto pertence.

O segundo vídeo, chamado Objeto Aprendido, faz o robô gravar uma foto do ambiente, e depois gravar uma segunda foto com um objeto na frente. Dessa forma, ele faz a subtração do objeto do fundo e "aprende" o que deve ser o objeto real. 

Em ambos vídeos você verá o robô seguindo seu alvo e desviando de obstáculos com seu laser, além de recuar e se afastar de objetos nos quais ele bater, ação permitida pelos bumpers localizados na região frontal.

--- Criação ---

O projeto em si foi feito ao longo das aulas e atendimentos fornecidos, além de certa parte ter sido elaborada em casa, nos fatidicos finais de semana! Uma certa divisão de trabalho foi feita, o Hugo e a Sabrina começaram trabalhando na parte de visão e filtro de imagem, estudando a camerâ do robô e tentando criar filtros e mascaras para o robô enxergar. Enquanto isso, o Jean se dedicou a ver como o ROS (robot operational system) recebe as variáveis importantes do Neato, como velocidade das rodas, rotação, correr, parar etc. O importante é que até o final do projeto, todos os membros do grupo estavam 100% integrados em ambos códigos, sabendo como o robô funcionava em todos os segmentos.

Dois arquivos foram elaborados para este projeto. O arquivo Follow.py, que implementa todos os filtros de imagem e define O QUE o robô deve seguir. Já o arquivo localizar.py implementa COMO o robô vai seguir tal objeto, a velocidade com que vai ir atras dele, e o que fazer quando o objeto sumir. Além disso, esse código implementa as funções de sobrevivência do robô.
