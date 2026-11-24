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
 # 30/11 (seg)
 'post-39-era-so-isso': [
  dict(t='capa', bg=W, k='Carreira', h='Lançava, conciliava, pagava... e o cliente achava que [era só isso]', sub='Cena hipotética.', size=84),
  dict(k='Cena hipotética', h='A rotina que o cliente vê.', b='Lançar contas, conciliar o banco, agendar o que ele aprovou. Tudo em dia, e ele ainda acha que o serviço é "digitar".'),
  dict(k='O que ele não vê', h='Conferência e relatório.', b='Saldo batido com o extrato, categoria revisada, relatório que fecha.'),
  dict(k='Comunicação', h='Avisar antes de o problema chegar.', b='Conta que vence sem saldo, recebimento atrasado, comprovante que falta.'),
  dict(bg=K, k='O salto', h='Explicar o que os números dizem.', b='Quando você mostra o resultado, o cliente para de enxergar só o lançamento.'),
  dict(bg=G, k='Resumo', h='Lançar é a base. A&nbsp;análise é o que o cliente lembra.'),
  cta('No grupo', 'Quer trocar ideia sobre isso? O grupo está no link da bio.'),
 ],
 # 01/12 (ter)
 'post-40-voce-trabalha-com-bpo-quando': [
  dict(t='capa', foto=BI+'pessoas-trabalhando/foto-01-analista-notebook-perfil.png', k='Identificação', h='Você trabalha&nbsp;com BPO [quando...]', sub='Complete a frase nos comentários.', size=92),
  dict(k='Você trabalha com BPO quando', h='...abre o extrato antes do café.', cls='grande'),
  dict(bg=K, k='Você trabalha com BPO quando', h='...sabe de cabeça qual cliente paga em qual dia.', cls='grande'),
  dict(k='Você trabalha com BPO quando', h='...já explicou o que é BPO três vezes na mesma festa.', cls='grande'),
  dict(bg=K, k='Você trabalha com BPO quando', h='...sente que falta um lançamento antes de saber qual.', cls='grande'),
  dict(bg=G, k='Você trabalha com BPO quando', h='...comemora a conciliação que fecha de primeira.', cls='grande'),
  cta('Mande para alguém', 'Mande para o colega que vai se reconhecer.'),
 ],
 # 02/12 (qua)
 'post-41-vou-pensar': [
  dict(t='capa', foto=BI+'reuniao-com-cliente/foto-11-consultor-relatorio-cliente.png', k='Gestão de clientes', h='O cliente disse "vou&nbsp;pensar"? Responda com [esta pergunta]', size=84),
  dict(k='Cena hipotética', h='A reunião foi boa. A&nbsp;resposta, nem tanto.', b='Você apresentou o serviço, o cliente gostou e, no fim, veio o "vou pensar".'),
  dict(bg=K, k='Por que acontece', h='Ele compara com o que já conhece.', b='Se a referência dele é "alguém que lança as contas", qualquer preço parece alto.'),
  dict(t='num', n='01', k='Escopo antes do preço', h='Mostre o que está incluído.', b='Tarefa por tarefa, antes de falar em valor.'),
  dict(t='num', n='02', k='O que ele deixa de fazer', h='Mostre o tempo que volta para ele.', b='Conferir extrato, cobrar comprovante, montar planilha no domingo.'),
  dict(t='num', n='03', k='Próximo passo', h='Combine o que acontece depois.', b='Uma data para a resposta, ou uma dúvida para tirar antes dela.'),
  dict(bg=G, k='A pergunta', h='"O que falta para você decidir?"', b='A resposta mostra se a dúvida é preço, escopo ou momento.'),
  cta('Mande para alguém', 'Mande para quem ouviu "vou pensar" esta semana.'),
 ],
 # 03/12 (qui)
 'post-42-conferir-relatorio': [
  dict(t='capa', bg=G, k='Rotina e processo', h='Antes de clicar em "enviar" no relatório, confira estas [4 coisas]', size=90),
  dict(t='num', n='01', k='Saldos', h='Os saldos batem com o extrato?', b='Conta por conta, no último dia do período.'),
  dict(t='num', n='02', k='Classificação', h='Os lançamentos estão na categoria certa?', b='Olhe primeiro os valores maiores e o que caiu em "outros".'),
  dict(t='num', n='03', k='Comparativo', h='O que mudou em relação ao mês anterior?', b='Coloque os dois meses lado a lado.'),
  dict(t='num', n='04', k='Variações', h='Cada variação grande tem explicação?', b='Se você não sabe explicar, o cliente vai perguntar.'),
  dict(foto=BI+'documentos-e-relatorios/foto-08-analista-grafico-impresso.png', k='Se der', h='Peça um segundo olhar.', b='Outra pessoa acha em minutos o que você já não enxerga.'),
  dict(t='lista', bg=K, k='Resumo', h='Antes de enviar:', itens=['Saldos', 'Classificação', 'Comparativo', 'Variações']),
  cta('Salve', 'Salve para conferir no próximo fechamento.'),
 ],
 # 04/12 (sex)
 'post-43-ferramentas': [
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
