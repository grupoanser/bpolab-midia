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
 # 23/11 (seg)
 'post-34-favorzinho-fora-do-contrato': [
  dict(t='capa', bg=K, k='Gestão de clientes', h='O cliente pediu "só um [favorzinho"] fora do contrato?', sub='Leia antes de aceitar.', size=96),
  dict(k='Cena hipotética', h='Começa com um pedido avulso.', b='"Liga para esse fornecedor e negocia o prazo?" Uma vez vira duas. Em três meses, já faz parte da rotina, sem estar no preço.'),
  dict(bg=K, k='O problema', h='O que você faz sem combinar vira obrigação.', b='Depois fica difícil cobrar por algo que você já fazia sem custo.'),
  dict(t='num', n='01', k='Escopo', h='Liste o que entra.', b='Tarefas, contas e prazos que fazem parte do serviço.'),
  dict(t='num', n='02', k='Fora do escopo', h='Liste o que fica de fora.', b='E diga como funciona um pedido extra: orçamento à parte ou revisão do contrato.'),
  dict(t='num', n='03', k='Revisão', h='Reveja o combinado de tempos em tempos.', b='Se o pedido avulso virou rotina, ele entra no escopo e no preço.'),
  dict(bg=G, k='Contrato', h='Para o texto do contrato, consulte um profissional.', b='O escopo você conhece melhor que ninguém. A redação fica com quem é da área.'),
  cta('Comente', 'Já passou por isso?'),
 ],
 # 24/11 (ter)
 'post-35-comecou-com-um-cliente': [
  dict(t='capa', bg=W, k='Começar no BPO', h='Começamos em 2020 com [um cliente só]', sub='Para começar, você não precisa de carteira.', size=100),
  dict(k='O mito', h='"Só vou começar quando tiver vários clientes."', b='Esperar a carteira pronta adia o primeiro passo.'),
  dict(k='O primeiro cliente', h='É ele que ensina a rotina na prática.', b='Prazo real, documento que atrasa, dúvida que você não tinha previsto.'),
  dict(bg=K, k='Capacidade', h='Não aceite mais do que consegue entregar.', b='Um cliente bem atendido pesa mais do que vários atendidos pela metade.'),
  dict(k='Indicação', h='Boa entrega costuma abrir a conversa com o próximo.', b='Quem gostou do serviço comenta com outro empresário.'),
  dict(bg=G, k='Resumo', h='Para começar, um cliente basta.', b='O resto vem com entrega e paciência.'),
  cta('Comente', 'Foi assim com você?'),
 ],
 # 25/11 (qua)
 'post-36-3-numeros-relatorio': [
  dict(t='capa', bg=G, k='Análise de resultado', h='O cliente não entende seu relatório? Comece por estes [3 números]', size=88),
  dict(foto=BI+'documentos-e-relatorios/foto-02-maos-relatorios-pasta-verde.png', k='Antes da tabela', h='Três números, uma frase para cada.', b='O resto do relatório fica de apoio.'),
  dict(t='num', n='01', k='Margem', h='Quanto sobra do que a empresa vende.', b='Frase para o cliente: "depois dos custos, isto é o que fica com a empresa".'),
  dict(t='num', n='02', k='Caixa projetado', h='Quanto vai ter na conta nas próximas semanas.', b='Frase para o cliente: "se nada mudar, este é o saldo no dia tal".'),
  dict(t='num', n='03', k='Inadimplência', h='Quanto está atrasado para receber.', b='Frase para o cliente: "isto já devia ter entrado e ainda não entrou".'),
  dict(t='lista', bg=K, k='Resumo', h='Comece por:', itens=['Margem', 'Caixa projetado', 'Inadimplência']),
  cta('Comente', 'Quais números você mostra ao seu cliente?'),
 ],
 # 26/11 (qui)
 'post-37-3-prompts-dados-simulados': [
  dict(t='capa', bg=K, k='IA e ferramentas', h='3 [prompts] para a rotina do BPO', sub='Com dados simulados. Salve para testar.', size=104),
  dict(k='Antes de tudo', h='Use dados simulados.', b='Troque nome de cliente, CNPJ e valores reais por dados fictícios antes de colar em qualquer ferramenta.'),
  dict(t='num', n='01', k='Classificar lançamentos', h='"Sugira uma categoria para cada lançamento abaixo e avise quando estiver em dúvida."', b='Cole a lista simulada e o seu plano de contas.', size=60),
  dict(t='num', n='02', k='Resumir variações', h='"Compare os dois meses abaixo e liste as maiores variações por categoria."', b='Você confere e escreve a explicação.', size=60),
  dict(t='num', n='03', k='Mensagem ao cliente', h='"Escreva uma mensagem curta e educada pedindo os comprovantes desta lista."', b='Ajuste o tom antes de enviar.', size=60),
  dict(bg=G, k='Sempre', h='Revise antes de usar.', b='A IA entrega um rascunho. Quem responde pelo resultado é você.'),
  cta('Salve', 'Salve para testar na sua rotina.'),
 ],
 # 27/11 (sex)
 'post-38-crescer-sem-virar-dono': [
  dict(t='capa', bg=W, k='Carreira', h='Dá para crescer no BPO [sem virar dono]?', sub='Quatro caminhos possíveis. Nenhum é promessa.', size=100),
  dict(t='num', n='01', k='Especializar-se', h='Ficar muito bom em um tipo de cliente ou de tarefa.', b='Análise, conciliação de alto volume ou um setor específico.'),
  dict(t='num', n='02', k='Liderar equipe', h='Coordenar analistas e revisar o trabalho.', b='Menos operação, mais conferência e gestão de pessoas.'),
  dict(t='num', n='03', k='Por conta própria', h='Atender seus clientes como autônomo.', b='Mais liberdade e mais responsabilidade pela venda e pela entrega.'),
  dict(t='num', n='04', k='Consultoria', h='Ajudar empresas a organizar o financeiro.', b='Projetos com começo e fim, em vez de rotina mensal.'),
  dict(foto=BI+'pessoas-trabalhando/foto-04-analista-notebook-blazer.png', k='Cada caminho tem custo', h='Tempo, estudo ou risco.', b='Escolha pelo tipo de trabalho que você gosta de fazer.'),
  cta('Comente', 'Onde você quer chegar?'),
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
