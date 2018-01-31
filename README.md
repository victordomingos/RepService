# RepService
Aplicação de base de dados para registo em loja de processos de garantia e reparações. Permite manter um registo dos artigos entregues pelos clientes, do seu percurso durante a tramitação do processo e da comunicação realizada. Os processos que requerem atenção, por exemplo devido a atrasos na entrega ou na receção de comunicação de cliente são destacados na lista principal, por forma a permitir uma intervenção em conformidade.

## Capturas de ecrã
1. Janela de autenticação:

![login](https://user-images.githubusercontent.com/18650184/35652209-8da74808-06da-11e8-88ed-3e31d4b6e71c.png)

2. Aspeto geral da aplicação (lista de reparações com painel de mensagens, janelas de detalhes de reparações e de mensagens/eventos):

![service_msg_reparacoes](https://user-images.githubusercontent.com/18650184/27431379-4a942e82-5744-11e7-87cb-226f798a5bba.jpg)

3. Formulários de introdução de dados (nova reparação de artigo de stock, nova remessa):

![service_rep_stock_e_remessas](https://user-images.githubusercontent.com/18650184/27431380-4abc89cc-5744-11e7-9c00-4ed3e39ddebd.jpg)

4. Formulários de introdução de dados (nova reparação de artigo de cliente, novo contacto):

![service_rep_cliente_e_contactos](https://user-images.githubusercontent.com/18650184/27431381-4ac27404-5744-11e7-804a-d4b5d58e7435.jpg)


## Dependências
Esta aplicação é desenvolvida em Python 3.6 e tkinter, a partir de uma ideia original de Márcio Araújo.

Requer, na versão atual o(s) seguinte(s) módulo(s) externo(s):

- Python MegaWidgets 2.0.1
- SQL Alchemy 1.1.5


O desenvolvimento e testes têm sido realizados apenas em Mac, no entanto deverá ser bastante simples a adaptação para funcionar sem problemas em Windows ou Linux. Em sistemas operativos antigos, alguns ícones Unicode poderão não aparecer corretamente. Em ambiente Mac, é altamente recomendável usar o ActiveTCL 8.5.18, conforme as notas de lançamento da linguagem Python, de modo a assegurar a compatibilidade e estabilidade do tkinter no OS X.


## Como usar
Para iniciar a aplicação, basta executar o ficheiro `service/service.py` com o interpretador Python 3.6 ou superior.
