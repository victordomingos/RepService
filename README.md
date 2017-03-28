# RepService
Aplicação de base de dados para registo em loja de processos de garantia e reparações. Permite manter um registo dos artigos entregues pelos clientes, do seu percurso durante a tramitação do processo e da comunicação realizada. Os processos que requerem atenção, por exemplo devido a atrasos na entrega ou na receção de comunicação de cliente são destacados na lista principal, por forma a permitir uma intervenção em conformidade.

![screenshot_repservice_v0 4](https://cloud.githubusercontent.com/assets/18650184/24384268/80fdcdda-135a-11e7-8988-338bdfd18201.png)

## Dependências
Esta aplicação é desenvolvida em Python 3.6 e tkinter, a partir de uma ideia original de Márcio Araújo.

Requer, ou melhor, prevê-se que venha a requerer, os seguintes módulos externos:

- SQLalchemy 1.1.5
- PyMySQL 0.7.10
- ReportLab 3.4.0

O desenvolvimento e testes têm sido realizados apenas em Mac, no entanto deverá ser bastante simples a adaptação para funcionar sem problemas em Windows ou Linux. Em sistemas operativos antigos, alguns ícones Unicode poderão não aparecer corretamente. Em ambiente Mac, é altamente recomendável usar o ActiveTCL 8.5.18, conforme as notas de lançamento da linguagem Python, de modo a assegurar a compatibilidade e estabilidade do tkinter no OS X.
