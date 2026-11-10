"""Gerador de carrossel BPO Lab, estilo do post 16 (1080x1350).
Uso: python3 marca/gerador-v2.py  (gera todos os posts definidos em POSTS)
"""
import asyncio, base64, os
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def b64(p): return base64.b64encode(open(os.path.join(ROOT, p), 'rb').read()).decode()
SIM_K = b64('marca/simbolo-escuro.png'); SIM_W = b64('marca/simbolo-branco.png')
G = '#A1D141'; K = '#111111'; O = '#F6F6F2'; W = '#FFFFFF'

def nb(t):
    # evita palavra sozinha na última linha: une as duas últimas palavras
    if not t or '<' in t or ' ' not in t.strip(): return t
    a, b = t.rstrip().rsplit(' ', 1); return a + '&nbsp;' + b

def hl(t): t = nb(t); return t.replace('BPO Lab', 'BPO&nbsp;Lab').replace('[', '<span class="hl">').replace(']', '</span>')

def slide(s, i, n):
    bg = s.get('bg', O); dark = bg == K or s.get('foto')
    fg = W if dark else K
    kc = G if dark else ('#111' if bg == G else '#444')
    logo = SIM_W if dark else SIM_K
    t = s.get('t', 'texto')
    foto = ''
    if s.get('foto'):
        foto = f'<div class="foto" style="background-image:url(data:image/png;base64,{b64(s["foto"])})"></div><div class="shade"></div>'
    inner = ''
    if t == 'capa':
        inner = f'<div class="kick">{s["k"]}</div><h1 class="cap">{hl(s["h"])}</h1>' + (f'<p class="sub">{nb(s["sub"])}</p>' if s.get('sub') else '')
        pos = 'end' if s.get('foto') else 'center'
    elif t == 'num':
        inner = f'<div class="num">{s["n"]}</div><div class="kick">{s["k"]}</div><h2>{hl(s["h"])}</h2>' + (f'<p class="body">{nb(s["b"])}</p>' if s.get('b') else '')
        pos = 'center'
    elif t == 'lista':
        items = ''.join(f'<li><span class="box">{j+1}</span>{x}</li>' for j, x in enumerate(s['itens']))
        inner = f'<div class="kick">{s["k"]}</div><h2>{hl(s["h"])}</h2><ol class="lst">{items}</ol>'
        pos = 'center'
    else:
        inner = f'<div class="kick">{s["k"]}</div><h2 class="{s.get("cls","")}">{hl(s["h"])}</h2>' + (f'<p class="body">{nb(s["b"])}</p>' if s.get('b') else '')
        pos = 'end' if s.get('foto') else 'center'
    dots = ''.join(f'<i class="{"on" if j == i else ""}"></i>' for j in range(n))
    arr = '' if i == n - 1 else 'ARRASTA &rarr;'
    hlbg = G; hlfg = K
    if bg == G: hlbg = K; hlfg = G
    return f'''<html><head><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:{bg};color:{fg};font-family:Poppins,sans-serif;position:relative;overflow:hidden}}
.foto{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(17,17,17,.15) 0%,rgba(17,17,17,.35) 40%,rgba(17,17,17,.92) 72%,#111 100%)}}
.logo{{position:absolute;left:84px;top:72px;width:80px;z-index:2}}
.wrap{{position:absolute;left:84px;right:84px;top:200px;bottom:200px;display:flex;flex-direction:column;justify-content:{pos};z-index:2}}
.kick{{font-weight:700;font-size:28px;letter-spacing:6px;color:{kc};margin-bottom:26px;text-transform:uppercase}}
h1.cap{{font-weight:700;font-size:{s.get('size',104)}px;line-height:1.16;letter-spacing:-1.5px}}
h2{{font-weight:700;font-size:{s.get('size',72)}px;line-height:1.13;letter-spacing:-1px}}
h2.grande{{font-size:84px}}
.hl{{background:linear-gradient(transparent 14%,{hlbg} 14%);color:{hlfg};padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.sub{{font-size:40px;line-height:1.4;margin-top:40px;font-weight:400}}
.body{{font-size:40px;line-height:1.45;margin-top:40px;font-weight:400}}
.num{{font-weight:800;font-size:220px;line-height:.9;color:{G};letter-spacing:-6px;margin-bottom:30px}}
.lst{{list-style:none;margin-top:40px;display:flex;flex-direction:column;gap:26px}}
.lst li{{display:flex;align-items:center;gap:28px;font-weight:700;font-size:62px;line-height:1.1}}
.box{{flex:none;width:72px;height:72px;background:{K if not dark else G};color:{G if not dark else K};display:flex;align-items:center;justify-content:center;font-size:40px}}
.foot{{position:absolute;left:84px;right:84px;bottom:76px;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:26px;z-index:2}}
.dots{{display:flex;gap:10px}} .dots i{{width:12px;height:12px;border-radius:50%;background:{fg};opacity:.3}} .dots i.on{{opacity:1}}
.at{{color:{G if dark else K};font-weight:700}}
</style></head><body>{foto}
<img class="logo" src="data:image/png;base64,{logo}">
<div class="wrap">{inner}</div>
<div class="foot"><span>{i+1:02d}/{n:02d}</span><span class="dots">{dots}</span><span>{arr}</span></div>
</body></html>'''

def cta(k, h, extra='@bpo.lab'):
    return dict(bg=K, k=k, h=h, b=f'<span class="at">{extra}</span>')

BI = 'banco-de-imagens/'
POSTS = {
 # 12/11 (qui)
 'post-23-semana-analista': [
  dict(t='capa', bg=W, k='Rotina e processo', h='Se a sua segunda começa apagando [incêndio], mude o que você faz na sexta', sub='Um modelo de semana para adaptar à sua rotina.', size=84),
  dict(foto=BI+'documentos-e-relatorios/foto-12-homem-organizando-papeis.png', k='A ideia', h='Cada dia da semana com uma tarefa principal.', b='O resto encaixa em volta dela.'),
  dict(k='Segunda', h='Vencimentos da semana.', b='Veja o que vence até sexta e o que ainda depende de aprovação do cliente.', cls='grande'),
  dict(bg=K, k='Todo dia', h='Conciliação do banco.', b='Uns minutos por dia evitam a pilha do fim do mês.', cls='grande'),
  dict(k='Terça e quarta', h='Lançamentos e classificação.', b='Com o banco em dia, a semana não acumula.', cls='grande'),
  dict(k='Quinta', h='Pendências com os clientes.', b='Documento que falta, lançamento sem explicação, dúvida para tirar. Tudo junto, em uma mensagem só.', cls='grande'),
  dict(bg=K, k='Sexta', h='Relatórios e comunicação.', b='Quem fecha a semana com o cliente informado começa a segunda sem surpresa.', cls='grande'),
  dict(bg=G, k='Importante', h='Isto é um modelo, não uma regra.', b='Ajuste ao número de clientes e aos prazos de cada um.'),
  cta('Comente', 'Como é a sua semana hoje?'),
 ],
 # 13/11 (sex)
 'post-24-mito-ia': [
  dict(t='capa', bg=G, k='Mito', h='Usar IA é [trapacear] no trabalho?', sub='A opinião do BPO&nbsp;Lab.', size=104),
  dict(k='O que a IA entrega', h='Um rascunho. A resposta final é sua.', b='Ela sugere uma classificação, resume um extrato, escreve a primeira versão de um <span style="white-space:nowrap">e-mail</span>. Quem decide é você.'),
  dict(bg=K, k='Continua com você', h='Julgamento, conferência e a relação com o cliente.', b='Nenhuma ferramenta conhece o cliente como quem o atende toda semana.'),
  dict(t='num', n='01', k='Regra', h='Revise tudo o que a IA produzir.', b='Se você não consegue explicar o resultado, ele não vai para o cliente.'),
  dict(t='num', n='02', k='Regra', h='Dado real de cliente só com autorização.', b='Na dúvida, troque nomes e valores por dados fictícios antes de colar.'),
  dict(bg=G, k='O ganho', h='O tempo que sobra vai para a análise.', b='É ali que o cliente enxerga valor.'),
  cta('Comente', 'Você usa IA no trabalho? Para quê?'),
 ],
 # 14/11 (sáb)
 'post-25-checklist-primeiro-cliente': [
  dict(t='capa', bg=K, k='Começar no BPO', h='Checklist: antes de fechar seu [primeiro cliente]', sub='Salve para usar na próxima conversa.', size=96),
  dict(foto=BI+'mentoria-e-treinamento/foto-13-dupla-revisando-documento.png', k='Antes de começar', h='Combine por escrito o que vai ser feito.', b='O que não foi combinado vira cobrança depois.'),
  dict(t='num', n='01', k='Escopo', h='Escopo escrito.', b='Quais tarefas entram e quais ficam de fora.'),
  dict(t='num', n='02', k='Contas', h='Contas e bancos.', b='Quais contas, cartões e bancos você vai acompanhar.'),
  dict(t='num', n='03', k='Pagamentos', h='Quem aprova os pagamentos.', b='O BPO organiza. Quem aprova é o cliente.'),
  dict(t='num', n='04', k='Prazos', h='Prazo dos documentos.', b='Até que dia o cliente manda notas, boletos e comprovantes.'),
  dict(t='num', n='05', k='Comunicação', h='Canal de conversa.', b='Onde vocês falam e em que horário.'),
  dict(t='num', n='06', k='Contrato', h='Contrato revisado.', b='Peça para um advogado revisar antes de assinar.'),
  dict(t='lista', bg=G, k='Resumo', h='Antes do primeiro cliente:', itens=['Escopo', 'Contas e bancos', 'Aprovação', 'Prazos', 'Canal', 'Contrato']),
  cta('Salve', 'Salve para usar antes do primeiro cliente.'),
 ],
 # 15/11 (dom)
 'post-26-dre-dfc': [
  dict(t='capa', bg=W, k='Análise de resultado', h='Quando o cliente perguntar "cadê o lucro?", a resposta não está na [DRE]', size=84),
  dict(k='DRE', h='A empresa teve lucro no período?', b='Mostra receitas, custos e despesas pela competência: quando a venda ou a despesa aconteceu.'),
  dict(bg=K, k='DFC', h='Para onde foi o dinheiro?', b='Mostra entradas e saídas pelo caixa: quando o dinheiro entrou ou saiu da conta.'),
  dict(k='Exemplo hipotético', h='Uma venda grande a prazo.', b='Na DRE, ela entra no mês da venda e o lucro aparece. No caixa, o dinheiro só chega quando o cliente pagar.'),
  dict(k='Por isso', h='Dá para ter lucro e faltar dinheiro.', b='Estoque comprado, parcelas a receber e empréstimo pago tiram caixa sem pesar no lucro do mesmo jeito.'),
  dict(bg=G, k='Resumo', h='A DRE diz se deu lucro. A DFC diz onde está o dinheiro.', b='Leia os dois juntos.'),
  cta('Comente', 'Qual dos dois você mais usa com seus clientes?'),
 ],
 # 16/11 (seg)
 'post-27-horas-por-cliente': [
  dict(t='capa', foto=BI+'pessoas-trabalhando/foto-15-analista-dois-monitores.png', k='Gestão de clientes', h='Se dois clientes pagam igual e um dá o [dobro de trabalho], revise isto', size=84),
  dict(k='A situação', h='Mesmo valor, esforço diferente.', b='Um manda tudo organizado. O outro manda comprovante por foto, fora do prazo, e pede ajuste toda semana.'),
  dict(t='num', n='01', k='Passo 1', h='Anote as horas de cada cliente por 30 dias.', b='Planilha simples: data, cliente, tarefa e tempo gasto.'),
  dict(t='num', n='02', k='Passo 2', h='Compare as horas com o que cada um paga.', b='Exemplo hipotético: A e B pagam o mesmo, mas B consome muito mais horas.'),
  dict(t='num', n='03', k='Passo 3', h='Ajuste o escopo ou o preço.', b='Com o registro em mãos, a conversa com o cliente sai do achismo.'),
  dict(bg=G, k='Antes de reajustar', h='Às vezes o problema é processo, e não preço.', b='Um prazo de envio combinado pode resolver sem mexer no valor.'),
  cta('Comente', 'Você mede as horas de cada cliente?'),
 ],
 # 17/11 (ter)
 'post-28-primeira-conversa': [
  dict(t='capa', foto=BI+'reuniao-com-cliente/foto-10-consultor-restaurante.png', k='Começar no BPO', h='Na primeira conversa com um cliente, esta [pergunta] revela mais que todas', size=84),
  dict(t='lista', bg=O, k='Para entender o cenário', h='Comece por estas:', itens=['Como controla hoje?', 'Quem paga e quem aprova?', 'Onde fica o registro?']),
  dict(bg=K, k='A pergunta', h='"O que mais atrapalha o seu financeiro hoje?"', b='A resposta mostra a dor real. E é ela que vai guiar o escopo.'),
  dict(k='Escute', h='Deixe o cliente falar sem interromper.', b='Anote as palavras dele. Elas vão para a proposta.'),
  dict(bg=G, k='Cuidado', h='Não prometa resultado na primeira conversa.', b='Proponha um escopo claro do que você vai fazer.'),
  cta('Comente', 'Que pergunta você acrescentaria?'),
 ],
 # 18/11 (qua)
 'post-29-nicho-generalista': [
  dict(t='capa', bg=W, k='Nicho ou generalista', h='Atendia qualquer tipo de empresa, aceitava todo cliente e não conseguia [padronizar] nada', sub='Uma situação comum no começo.', size=80),
  dict(k='Nicho', h='Você aprende o vocabulário e as rotinas de um setor.', b='Os processos se repetem, e fica mais fácil padronizar.'),
  dict(k='Generalista', h='Cada cliente traz uma rotina diferente.', b='Você aprende muito, mas leva mais tempo para criar um padrão.'),
  dict(bg=K, k='Risco do nicho', h='Depender de um setor só.', b='Se o setor passa por um ano ruim, a sua carteira sente junto.'),
  dict(bg=K, k='Risco do generalista', h='Saber um pouco de tudo.', b='E não ser lembrado como referência em nada.'),
  dict(k='Como testar', h='Olhe para os clientes que você já tem.', b='Se mais de um é do mesmo setor, comece por ele. Sem fechar a porta para os outros.'),
  dict(bg=G, k='Sem certo ou errado', h='A escolha depende do seu momento.', cls='grande'),
  cta('Comente', 'Nicho ou generalista: qual você escolheu?'),
 ],
 # 19/11 (qui)
 'post-30-conferir-relatorio': [
  dict(t='capa', bg=G, k='Rotina e processo', h='Antes de clicar em "enviar" no relatório, confira estas [4 coisas]', size=90),
  dict(t='num', n='01', k='Saldos', h='Os saldos batem com o extrato?', b='Conta por conta, no último dia do período.'),
  dict(t='num', n='02', k='Classificação', h='Os lançamentos estão na categoria certa?', b='Olhe primeiro os valores maiores e o que caiu em "outros".'),
  dict(t='num', n='03', k='Comparativo', h='O que mudou em relação ao mês anterior?', b='Coloque os dois meses lado a lado.'),
  dict(t='num', n='04', k='Variações', h='Cada variação grande tem explicação?', b='Se você não sabe explicar, o cliente vai perguntar.'),
  dict(foto=BI+'documentos-e-relatorios/foto-08-analista-grafico-impresso.png', k='Se der', h='Peça um segundo olhar.', b='Outra pessoa acha em minutos o que você já não enxerga.'),
  dict(t='lista', bg=K, k='Resumo', h='Antes de enviar:', itens=['Saldos', 'Classificação', 'Comparativo', 'Variações']),
  cta('Salve', 'Salve para conferir no próximo fechamento.'),
 ],
 # 20/11 (sex)
 'post-31-pov-primeira-semana': [
  dict(t='capa', bg=K, k='POV', h='Sua [primeira semana] no financeiro de uma empresa', sub='Cena hipotética: pastas misturadas, notas soltas e ninguém sabe o saldo certo.', size=96),
  dict(k='Dia 1', h='Mapear contas, bancos e cartões.', b='Antes de lançar qualquer coisa, saiba por onde o dinheiro passa.', cls='grande'),
  dict(k='Dia 2', h='Levantar as pendências.', b='Contas em atraso, notas sem lançamento, comprovantes perdidos. Faça uma lista.', cls='grande'),
  dict(k='Dia 3', h='Definir a rotina.', b='O que vai ser feito todo dia, toda semana e no fim do mês.', cls='grande'),
  dict(bg=K, k='Dias 4 e 5', h='Entregar um primeiro relatório simples.', b='Saldo, o que vence e as pendências. Melhor simples e certo do que completo e atrasado.'),
  dict(bg=G, k='Na primeira semana', h='O objetivo é entender.', b='Arrumar vem depois.', cls='grande'),
  cta('Comente', 'Como foi a sua primeira semana em um financeiro?'),
 ],
 # 21/11 (sáb)
 'post-32-glossario-gerencial': [
  dict(t='capa', bg=W, k='Glossário 2', h='6 termos de [relatório gerencial] para ter na ponta da língua', sub='Salve para consultar.', size=92),
  dict(t='num', n='01', k='EBITDA', h='Lucro antes de juros, impostos, depreciação e amortização.', b='Mostra quanto a operação gera, sem o efeito de dívidas, tributos sobre o lucro e desgaste dos ativos.', size=64),
  dict(t='num', n='02', k='Margem de contribuição', h='Receita menos custos e despesas variáveis.', b='É o que sobra de cada venda para pagar os custos fixos e gerar lucro.'),
  dict(t='num', n='03', k='Ponto de equilíbrio', h='O faturamento em que não há lucro nem prejuízo.', b='Abaixo dele, a empresa perde dinheiro. Acima, começa a lucrar.'),
  dict(t='num', n='04', k='Capital de giro', h='O dinheiro para manter a operação rodando.', b='Cobre o intervalo entre pagar fornecedores e receber dos clientes.'),
  dict(t='num', n='05', k='CMV', h='Custo das mercadorias vendidas.', b='O custo do que saiu na venda, e não de tudo o que foi comprado no mês.'),
  dict(t='num', n='06', k='Ticket médio', h='Faturamento dividido pelo número de vendas.', b='Mostra quanto, em média, cada venda traz.'),
  dict(t='lista', bg=G, k='Resumo', h='Os 6 termos:', itens=['EBITDA', 'Margem de contribuição', 'Ponto de equilíbrio', 'Capital de giro', 'CMV', 'Ticket médio']),
  cta('Salve', 'Salve para consultar no próximo relatório.'),
 ],
 # 22/11 (dom)
 'post-33-ferramentas': [
  dict(t='capa', bg=G, k='Comunidade', h='Qual [ferramenta] você usa no BPO?', sub='Vamos comparar nos comentários.', size=104),
  dict(k='Sistema financeiro', h='Onde ficam contas a pagar, a receber e o fluxo de caixa?'),
  dict(k='Planilha', h='Ainda faz parte da sua rotina?', b='Para controles paralelos, conferências ou relatórios.'),
  dict(bg=K, k='Conciliação', h='Como você bate o banco com os lançamentos?', b='Pelo próprio sistema, por planilha ou à mão.'),
  dict(k='IA', h='Entra em alguma parte do seu dia?', b='Classificação, resumo de extrato, rascunho de <span style="white-space:nowrap">e-mail</span>.'),
  dict(t='lista', bg=K, k='Na hora de escolher', h='Olhe para:', itens=['Integração com bancos', 'Custo por cliente', 'Tempo para aprender']),
  cta('Comente', 'Conte qual ferramenta você usa e por quê.'),
 ],
}

SO = os.environ.get('SO')
if SO: POSTS = {k: v for k, v in POSTS.items() if k == SO}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for pasta, slides in POSTS.items():
            out = os.path.join(ROOT, pasta); os.makedirs(out, exist_ok=True)
            for i, s in enumerate(slides):
                await pg.set_content(slide(s, i, len(slides)))
                await pg.wait_for_timeout(250)
                await pg.screenshot(path=os.path.join(out, f'slide{i+1}.png'))
        await b.close()
asyncio.run(main())
