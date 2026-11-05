"""Gerador de carrossel BPO Lab, estilo do post 16 (1080x1350).
Uso: python3 marca/gerador-v2.py  (gera todos os posts definidos em POSTS)
"""
import asyncio, base64, os
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def b64(p): return base64.b64encode(open(os.path.join(ROOT, p), 'rb').read()).decode()
SIM_K = b64('marca/simbolo-escuro.png'); SIM_W = b64('marca/simbolo-branco.png')
G = '#A1D141'; K = '#111111'; O = '#F6F6F2'; W = '#FFFFFF'

def hl(t): return t.replace('BPO Lab', 'BPO&nbsp;Lab').replace('[', '<span class="hl">').replace(']', '</span>')

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
        inner = f'<div class="kick">{s["k"]}</div><h1 class="cap">{hl(s["h"])}</h1>' + (f'<p class="sub">{s["sub"]}</p>' if s.get('sub') else '')
        pos = 'end' if s.get('foto') else 'center'
    elif t == 'num':
        inner = f'<div class="num">{s["n"]}</div><div class="kick">{s["k"]}</div><h2>{hl(s["h"])}</h2>' + (f'<p class="body">{s["b"]}</p>' if s.get('b') else '')
        pos = 'center'
    elif t == 'lista':
        items = ''.join(f'<li><span class="box">{j+1}</span>{x}</li>' for j, x in enumerate(s['itens']))
        inner = f'<div class="kick">{s["k"]}</div><h2>{hl(s["h"])}</h2><ol class="lst">{items}</ol>'
        pos = 'center'
    else:
        inner = f'<div class="kick">{s["k"]}</div><h2 class="{s.get("cls","")}">{hl(s["h"])}</h2>' + (f'<p class="body">{s["b"]}</p>' if s.get('b') else '')
        pos = 'center'
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
h1.cap{{font-weight:700;font-size:{s.get('size',104)}px;line-height:1.1;letter-spacing:-1.5px}}
h2{{font-weight:700;font-size:{s.get('size',72)}px;line-height:1.13;letter-spacing:-1px}}
h2.grande{{font-size:84px}}
.hl{{background:{hlbg};color:{hlfg};padding:0 14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
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

POSTS = {
 'post-17-termos-dfc': [
  dict(t='capa', bg=O, k='Glossário', h='5 termos de [DFC] que todo analista precisa dominar', sub='DFC é a Demonstração do Fluxo de Caixa. Salve para consultar.', size=96),
  dict(t='num', n='01', k='Fluxo operacional', h='O dinheiro da atividade do dia a dia.', b='Vendas e serviços recebidos, fornecedores, salários e impostos pagos. Mostra se a operação se paga.'),
  dict(t='num', n='02', k='Fluxo de investimento', h='O dinheiro que vai para ativos.', b='Compra e venda de máquinas, veículos, equipamentos e participações em outras empresas.'),
  dict(t='num', n='03', k='Fluxo de financiamento', h='O dinheiro que vem de sócios e de bancos.', b='Empréstimos tomados e pagos, aportes e retiradas dos sócios.'),
  dict(t='num', n='04', k='Saldo inicial e final', h='Quanto tinha no começo e quanto sobrou no fim.', b='Saldo inicial + entradas &minus; saídas = saldo final. E o saldo final tem que bater com o extrato.'),
  dict(t='num', n='05', k='Regime de caixa', h='Vale a data em que o dinheiro entrou ou saiu.', b='Venda de março recebida em abril entra na DFC de abril. Na DRE, que segue a competência, ela fica em março.'),
  dict(t='lista', bg=G, k='Resumo', h='Os 5 termos da DFC:', itens=['Operacional', 'Investimento', 'Financiamento', 'Saldo inicial e final', 'Regime de caixa']),
  cta('Salve', 'Salve para consultar na próxima DFC que você montar.'),
 ],
 'post-18-primeiro-cliente': [
  dict(t='capa', foto='banco-de-imagens/pessoas-trabalhando/foto-14-analista-telefone.png', k='Começar no BPO', h='Por que você ainda não fechou seu [primeiro cliente]?', sub='A resposta incomoda.', size=92),
  dict(k='O que não falta', h='Aula você já assistiu.', b='O que falta é o que vem depois dela.', cls='grande'),
  dict(k='A verdade', h='Ninguém fica 100% preparado antes do primeiro cliente.', b='A segurança vem com o trabalho, não antes dele.'),
  dict(k='O disfarce', h='Medo do primeiro passo parece cuidado.', b='Na prática, é adiar.'),
  dict(t='num', n='10', k='O primeiro passo', h='Liste 10 pessoas que têm empresa.', b='Mande mensagem para uma delas hoje. Só uma.'),
  dict(bg=G, k='O que ele precisa', h='Seu primeiro cliente precisa de uma conversa e de uma proposta escrita.', b='Não de um serviço perfeito.'),
  cta('Mande para alguém', 'Mande este post para quem está adiando.'),
 ],
 'post-19-pauta-encontro': [
  dict(t='capa', bg=K, k='Encontro · terça 10/11', h='O que você quer [discutir] na terça?', sub='1º encontro do BPO Lab, às 19h, no Google Meet.', size=100),
  dict(t='lista', bg=O, k='Vote na pauta', h='Escolha um número:', itens=['Conseguir cliente', 'Nicho ou generalista', 'Relatórios e análise', 'IA na rotina']),
  dict(bg=G, k='Outra pauta?', h='Tem outro assunto travando a sua rotina?', b='Escreva nos comentários. Sem dados de cliente.'),
  cta('Comente', 'Comente o número da sua pauta.', 'Para receber o link da chamada, entre no grupo pelo link da bio.'),
 ],
 'post-20-encontro-amanha': [
  dict(t='capa', bg=W, k='Amanhã · 19h', h='Amanhã tem [encontro] do BPO Lab', sub='O 1º encontro da comunidade. Terça, 10/11, às 19h, no Google Meet.', size=100),
  dict(k='Quando', h='Terça, 10/11, das 19h às 21h.', cls='grande'),
  dict(bg=K, k='Onde', h='No Google Meet.', b='O link da chamada é enviado no grupo.', cls='grande'),
  dict(bg=G, k='O que levar', h='Uma dúvida ou um caso da sua rotina.', b='Sem dados de cliente.'),
  cta('Como entrar', 'Ainda não está no grupo? Entre pelo link da bio.'),
 ],
 'post-21-encontro-hoje': [
  dict(t='capa', bg=G, k='Hoje · 19h', h='É hoje: [encontro] do BPO Lab', sub='Das 19h às 21h, no Google Meet.', size=110),
  dict(k='Como entrar', h='O link da chamada está no grupo.', b='Ainda não está? Entre pelo link da bio.'),
  dict(bg=K, k='O que levar', h='Uma dúvida.', b='Pode ser algo que travou ou algo que deu certo na sua rotina.', cls='grande'),
  cta('Até mais tarde', 'Te vejo às 19h.'),
 ],
}

POSTS['post-22-fechamento-um-dia'] = [
  dict(t='capa', bg=K, k='Rotina e processo', h='Se o seu fechamento leva mais de [um dia], o problema começa antes dele', size=84),
  dict(k='O jeito que trava', h='Acumular tudo para o fim do mês.', b='Extratos, comprovantes e pendências chegam juntos, e o fechamento vira correria.'),
  dict(bg=K, k='O jeito que flui', h='Conciliar todo dia e manter as pendências curtas.', b='No fim do mês, sobra só conferir.'),
  dict(k='No fechamento', h='Correria x conferência.', b='Quem acumula passa dias atrás de documento. Quem concilia todo dia só confere o que já está pronto.', cls='grande'),
  dict(k='No cliente', h='Informação atrasada x atualizada.', b='Com a conciliação em dia, o cliente sabe o saldo real desta semana, não só o do mês passado.'),
  dict(k='Como começar', h='Comece pelo banco mais movimentado.', b='Concilie só ele todo dia por uma semana. Depois, inclua os outros.'),
  dict(t='lista', bg=G, k='Resumo', h='Para fechar em 1 dia:', itens=['Conciliar todo dia', 'Pendências curtas', 'Começar pelo banco principal']),
  cta('Mande para alguém', 'Mande para quem fecha o mês em vários dias.'),
]
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
