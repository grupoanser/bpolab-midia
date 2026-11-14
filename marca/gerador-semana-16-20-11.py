import asyncio, base64, json, os, sys
from playwright.async_api import async_playwright

R = '/home/claude/bpolab-midia'
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
SIM = {k: b64(f'{R}/marca/{f}') for k,f in
       dict(dark='simbolo-escuro.png', white='simbolo-branco.png', green='simbolo-fundo-verde.png').items()}
FOTO = {
 'f09': b64(f'{R}/banco-de-imagens/reuniao-equipe/foto-09-dupla-anotando-reuniao.png'),
 'f16': b64(f'{R}/banco-de-imagens/documentos-e-relatorios/foto-16-mesa-notebook-proposta-calculadora.png'),
}
G='#A1D141'; K='#111111'; OFF='#F6F6F2'; W='#FFFFFF'
THEME = {
 'light': dict(bg=OFF, fg=K, muted='#6b6b66', sim='dark', dot='#cfcfc9', act=K, acc=G),
 'white': dict(bg=W,   fg=K, muted='#6b6b66', sim='dark', dot='#d9d9d4', act=K, acc=G),
 'dark':  dict(bg=K,   fg=OFF, muted=G, sim='white', dot='#444444', act='#FFFFFF', acc=G),
 'green': dict(bg=G,   fg=K, muted=K, sim='green', dot='rgba(17,17,17,.30)', act=K, acc=K),
}

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Poppins,sans-serif}
.sim{position:absolute;left:84px;top:70px;width:88px;height:88px;z-index:5}
.foot{position:absolute;left:90px;right:90px;bottom:62px;height:44px;display:flex;align-items:center;justify-content:space-between;z-index:5}
.cnt{font-weight:700;font-size:34px}
.dots{display:flex;gap:12px;position:absolute;left:50%;transform:translateX(-50%)}
.dots i{width:14px;height:14px;border-radius:50%;display:block}
.arr{font-weight:700;font-size:32px;letter-spacing:1px}
.wrap{position:absolute;left:90px;right:90px;top:300px;bottom:190px;display:flex;flex-direction:column;justify-content:flex-start}
.kick{font-weight:700;font-size:32px;letter-spacing:7px;text-transform:uppercase;margin-bottom:34px}
h1,h2{font-weight:700;letter-spacing:-1px;-webkit-text-stroke:1.6px currentColor}
h1{font-size:108px;line-height:1.12}
h2{font-size:68px;line-height:1.12}
mark{display:inline-block;padding:0 16px 4px;margin:0 -4px;line-height:1.08;border-radius:0;-webkit-text-stroke:1.6px currentColor}
p.b{font-size:44px;line-height:1.38;font-weight:400;margin-top:34px}
p.sub{font-size:44px;line-height:1.3;font-weight:400;margin-top:38px}
.num{font-weight:700;font-size:250px;line-height:.9;letter-spacing:-6px;-webkit-text-stroke:3px currentColor}
.stk{font-weight:700;font-size:64px;line-height:1.2;letter-spacing:-.5px;-webkit-text-stroke:1.2px currentColor}
.list{display:flex;flex-direction:column;gap:26px;margin-top:26px}
.li{display:flex;align-items:center;gap:30px;font-weight:700;font-size:64px;line-height:1.1;letter-spacing:-.5px;-webkit-text-stroke:1.2px currentColor}
.li b{flex:0 0 76px;width:76px;height:76px;background:#111;color:#A1D141;font-size:44px;display:flex;align-items:center;justify-content:center;-webkit-text-stroke:0}
.bar{width:120px;height:14px;border-radius:10px;margin:0 0 34px 0}
'''

def foot(i,n,t,last):
    dots=''.join(f'<i style="background:{t["act"] if k==i else t["dot"]}"></i>' for k in range(n))
    arr='' if last else '<div class="arr">ARRASTA →</div>'
    return f'<div class="foot" style="color:{t["fg"]}"><div class="cnt">{i+1:02d}/{n:02d}</div><div class="dots">{dots}</div>{arr}</div>'

def page(inner, t, i, n, extra_bg='', sim=None):
    simk = sim or t['sim']
    last = (i==n-1)
    return (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body style="background:{t["bg"]};color:{t["fg"]}">{extra_bg}'
            f'<img class="sim" src="data:image/png;base64,{SIM[simk]}">{inner}{foot(i,n,t,last)}</body></html>')

def mk(t, style=None):
    # style of highlight box
    if style=='dark': return f'background:{K};color:{G}'
    return f'background:{G};color:{K}'

def build(s, i, n):
    k = s['t']; t = THEME[k]; typ = s['type']
    if typ=='cover_photo':
        bg = (f'<div style="position:absolute;inset:0;background:url(data:image/png;base64,{FOTO[s["foto"]]}) {s.get("pos","center")}/cover"></div>'
              f'<div style="position:absolute;inset:0;background:linear-gradient(to top,#111 0%,#111 34%,rgba(17,17,17,.88) 48%,rgba(17,17,17,0) 74%)"></div>')
        inner = (f'<div class="wrap" style="justify-content:flex-end;bottom:200px;top:200px">'
                 f'<div class="kick" style="color:{G}">{s["kick"]}</div>'
                 f'<h1 style="color:#F6F6F2">{s["title"].replace("<mark>", "<mark style=\'"+mk(t)+"\'>")}</h1>'
                 f'<p class="sub" style="color:#F6F6F2">{s["sub"]}</p></div>')
        return page(inner, dict(t, sim='white'), i, n, bg, sim='white')
    if typ=='cover':
        style = 'dark' if k in ('green',) else None
        title = s['title'].replace('<mark>', "<mark style='"+mk(t, style)+"'>")
        inner = (f'<div class="wrap" style="justify-content:flex-end;top:200px;bottom:230px"><div class="kick" style="color:{t["muted"]}">{s["kick"]}</div>'
                 f'<h1 style="font-size:{s.get("fs",108)}px">{title}</h1><p class="sub">{s["sub"]}</p></div>')
        return page(inner, t, i, n)
    if typ=='cover_split':
        bg = (f'<div style="position:absolute;left:0;top:0;width:1080px;height:660px;background:url(data:image/png;base64,{FOTO[s["foto"]]}) right center/cover"></div>')
        title = s['title'].replace('<mark>', "<mark style='background:#111;color:#A1D141'>")
        inner = (f'<div style="position:absolute;left:90px;right:90px;top:720px;bottom:190px;display:flex;flex-direction:column;justify-content:center">'
                 f'<div class="kick" style="color:{K};margin-bottom:26px">{s["kick"]}</div>'
                 f'<h1 style="font-size:92px;line-height:1.16">{title}</h1><p class="sub" style="margin-top:28px">{s["sub"]}</p></div>')
        return page(inner, dict(t, sim='white'), i, n, bg, sim='white')
    if typ=='stake':
        inner = (f'<div class="wrap"><div class="bar" style="background:{G}"></div><div class="kick" style="color:{t["muted"]}">{s["kick"]}</div>'
                 f'<div class="stk">{s["text"]}</div></div>')
        return page(inner, t, i, n)
    if typ=='num':
        inner = (f'<div class="wrap"><div class="num" style="color:{G}">{s["n"]}</div>'
                 f'<div class="kick" style="color:{t["muted"]};margin-top:34px;margin-bottom:26px;font-size:30px">{s["kick"]}</div>'
                 f'<h2>{s["title"]}</h2><p class="b">{s["body"]}</p></div>')
        return page(inner, t, i, n)
    if typ=='text':
        inner = (f'<div class="wrap"><div class="bar" style="background:{G}"></div><div class="kick" style="color:{t["muted"]}">{s["kick"]}</div>'
                 f'<h2>{s["title"]}</h2><p class="b">{s["body"]}</p></div>')
        return page(inner, t, i, n)
    if typ=='flow':
        node = lambda lab, h, c, bgc, fgc: (f'<div style="background:{bgc};color:{fgc};border-radius:28px;padding:34px 40px;width:100%">'
              f'<div style="font-weight:700;font-size:30px;letter-spacing:6px">{lab}</div>'
              f'<div style="font-weight:700;font-size:56px;line-height:1.12;margin-top:12px;-webkit-text-stroke:1px currentColor">{h}</div>'
              f'<div style="font-size:38px;margin-top:10px;line-height:1.25">{c}</div></div>')
        inner = (f'<div class="wrap"><div class="kick" style="color:{t["muted"]};margin-bottom:30px">{s["kick"]}</div>'
                 + node(s['a'][0], s['a'][1], s['a'][2], K, OFF)
                 + f'<div style="font-size:110px;font-weight:700;line-height:1;margin:10px 0 10px 50px;color:{G}">↓</div>'
                 + node(s['b'][0], s['b'][1], s['b'][2], G, K)
                 + f'<p class="b" style="font-size:40px;margin-top:36px;font-weight:700">{s["foot"]}</p></div>')
        return page(inner, t, i, n)
    if typ=='recap':
        items=''.join(f'<div class="li"><b>{j+1}</b><span style="font-size:{s.get("fs",64)}px">{x}</span></div>' for j,x in enumerate(s['items']))
        inner = (f'<div class="wrap"><div class="kick" style="color:{K}">{s["kick"]}</div><h2 style="margin-bottom:18px">{s["title"]}</h2><div class="list">{items}</div></div>')
        return page(inner, t, i, n)
    if typ=='cta':
        inner = (f'<div class="wrap" style="top:400px"><div class="kick" style="color:{G}">{s["kick"]}</div>'
                 f'<h2 style="font-size:{s.get("fs",72)}px">{s["title"]}</h2>'
                 f'<p class="b" style="color:{G};font-weight:700;font-size:56px;margin-top:44px;-webkit-text-stroke:1px {G}">@bpo.lab</p></div>')
        return page(inner, t, i, n)
    raise ValueError(typ)

def alt(s, i, n):
    pre = f'Slide {i+1} de {n}. '
    typ = s['type']
    if typ=='cover_photo' and s['foto']=='f09':
        return pre + f'Capa com foto gerada por IA de duas profissionais à mesa, uma anotando e outra explicando, com fundo escuro e título em letras brancas: {strip(s["title"])}. {s["sub"]}'
    if typ=='cover_split':
        return pre + f'Capa com foto gerada por IA de uma mesa escura vista de cima, com notebook, relatório, calculadora e caneta verde, e bloco verde com o título: {strip(s["title"])}. {s["sub"]}'
    if typ in ('cover',):
        return pre + f'Capa de fundo {"branco" if s["t"]=="white" else "preto" if s["t"]=="dark" else "verde"} com o título: {strip(s["title"])}. {s["sub"]}'
    if typ=='stake': return pre + f'Fundo off-white. Texto: {s["text"]}'
    if typ=='num': return pre + f'Fundo off-white, número {s["n"]} em verde. Título: {s["title"]}. Texto: {s["body"]}'
    if typ=='text': return pre + f'Fundo off-white. Título: {s["title"]}. Texto: {s["body"]}'
    if typ=='flow': return pre + f'Fundo off-white com dois blocos ligados por uma seta para baixo. {s["a"][0]}: {s["a"][1]}, {s["a"][2]}. {s["b"][0]}: {s["b"][1]}, {s["b"][2]}. {s["foot"]}'
    if typ=='recap': return pre + f'Fundo verde. {s["title"]} ' + ' '.join(f'{j+1}. {x}.' for j,x in enumerate(s['items']))
    if typ=='cta': return pre + f'Fundo preto. {s["title"]} @bpo.lab'
def strip(x): return x.replace('<br>',' ').replace('<mark>','').replace('</mark>','')

POSTS = {
 'post-17-4-duvidas-encontro': [
  dict(type='cover', t='green', kick='1º encontro', title='<mark>4 dúvidas</mark><br>do 1º encontro', sub='O que o grupo do BPO Lab trouxe.'),
  dict(type='stake', t='light', kick='Sobre o encontro', text='Quatro temas apareceram na conversa. Cada um vira um post nesta semana.'),
  dict(type='num', t='light', n='01', kick='Vender', title='Vender o primeiro contrato', body='Saber fazer não basta. É preciso chegar a quem tem empresa.'),
  dict(type='num', t='light', n='02', kick='Análise', title='Entregar DRE e DFC', body='Há quem faça só o operacional e tema prospectar sem saber montar a análise.'),
  dict(type='num', t='light', n='03', kick='Escopo', title='Proposta e escopo', body='Onde termina o seu trabalho? Sem isso escrito, o pedido avulso vira rotina.'),
  dict(type='num', t='light', n='04', kick='Pagamento', title='Pagamento e acesso ao banco', body='Quem programa, quem aprova e qual acesso você terá.'),
  dict(type='recap', t='green', kick='Resumo', title='Nesta semana:', items=['Vender', 'DRE e DFC', 'Proposta e escopo', 'Pagamento e acesso'], fs=62),
  dict(type='cta', t='dark', kick='Salve', title='Salve para acompanhar a semana.'),
 ],
 'post-18-4-perguntas-antes-do-preco': [
  dict(type='cover_photo', t='dark', foto='f09', pos='center top', kick='Primeira conversa', title='Antes do <mark>preço</mark>,<br>4 perguntas', sub='Faça na 1ª conversa com o cliente.'),
  dict(type='stake', t='light', kick='Por que importa', text='Preço sem diagnóstico vira chute. As respostas definem escopo e valor.'),
  dict(type='num', t='light', n='01', kick='Controle', title='Como controla hoje?', body='Banco, planilha, papel ou sistema. Entenda o ponto de partida.'),
  dict(type='num', t='light', n='02', kick='Aprovação', title='Quem paga e quem aprova?', body='Defina cedo quem decide cada pagamento. No BPO, quem aprova é o cliente.'),
  dict(type='num', t='light', n='03', kick='Registro', title='Onde fica o registro?', body='Extratos, notas, contratos: saiba onde estão e quem envia.'),
  dict(type='num', t='light', n='04', kick='Dor', title='O que mais atrapalha hoje?', body='A dor que o cliente nomeia sustenta o escopo. Não prometa resultado.'),
  dict(type='recap', t='green', kick='Resumo', title='As 4 perguntas:', items=['Como controla?', 'Quem paga e aprova?', 'Onde registra?', 'O que atrapalha?'], fs=58),
  dict(type='cta', t='dark', kick='Salve', title='Salve para a sua próxima primeira conversa.', fs=68),
 ],
 'post-19-primeiro-cliente-quem-atender': [
  dict(type='cover', t='white', kick='Vender', title='Primeiro cliente<br>de <mark>BPO</mark>?', sub='Comece escolhendo quem atender.'),
  dict(type='stake', t='light', kick='Por que importa', text='Escolher um tipo de empresa simplifica a venda e a rotina do começo.'),
  dict(type='text', t='light', kick='Serviços', title='Serviços têm fluxo mais linear', body='Escritórios, advogados e clínicas têm menos variações para controlar no início.'),
  dict(type='text', t='light', kick='Associações', title='Associações: pouco exploradas', body='Na nossa visão, é um segmento pouco atendido e que costuma pagar bem.'),
  dict(type='text', t='light', kick='Seu setor', title='Conhece um setor? Comece por ele', body='Vocabulário e rotina que você já domina encurtam a conversa de venda.'),
  dict(type='text', t='light', kick='Teste', title='Teste antes de se prender', body='Nicho de começo não é para sempre. Ajuste depois do primeiro contrato.'),
  dict(type='recap', t='green', kick='Resumo', title='Por onde começar:', items=['Serviços', 'Associações', 'O setor que você conhece'], fs=58),
  dict(type='cta', t='dark', kick='Envie', title='Envie para um colega que está escolhendo por onde começar.', fs=62),
 ],
 'post-20-quem-programa-nao-aprova': [
  dict(type='cover_split', t='green', foto='f16', kick='Pagamentos', title='Quem programa<br><mark>não aprova</mark>', sub='3 regras antes do primeiro pagamento.'),
  dict(type='stake', t='light', kick='Por que importa', text='Pagamento enviado para a pessoa errada tem custo e dono. Combine antes.'),
  dict(type='num', t='light', n='01', kick='Programar', title='Programar é com você', body='Você prepara o pagamento. O cliente decide se ele sai.'),
  dict(type='num', t='light', n='02', kick='Acesso', title='Acesso de operador no banco', body='Peça permissões limitadas. Evite o acesso master, principalmente quando a equipe crescer.'),
  dict(type='num', t='light', n='03', kick='Conferência', title='Conferência por escrito', body='Registre quem confere os dados do favorecido antes do envio. Contrato: consulte um profissional.'),
  dict(type='recap', t='green', kick='Resumo', title='3 regras:', items=['Você programa, o cliente aprova', 'Operador, não master', 'Quem confere, por escrito'], fs=46),
  dict(type='cta', t='dark', kick='Envie', title='Envie para um colega que vai assumir pagamentos de cliente.', fs=62),
 ],
 'post-21-cade-o-lucro': [
  dict(type='cover', t='dark', kick='DRE e DFC', title='Cadê o <mark>lucro</mark>?', fs=150, sub='A resposta não está só na DRE.'),
  dict(type='stake', t='light', kick='Por que importa', text='DRE e DFC respondem perguntas diferentes. Quem entrega só uma deixa o cliente sem a outra metade.'),
  dict(type='text', t='light', kick='DRE', title='Teve resultado?', body='Receitas, custos e despesas do período.'),
  dict(type='text', t='light', kick='DFC', title='Para onde foi o caixa?', body='O que entrou e saiu de dinheiro no período.'),
  dict(type='flow', t='light', kick='Venda a prazo', a=('OUTUBRO','Vendeu','A DRE mostra o resultado.'), b=('DEZEMBRO','Recebeu','A DFC mostra o caixa.'), foot='O resultado aparece antes do dinheiro.'),
  dict(type='text', t='light', kick='Juntos', title='Os dois contam a história', body='Resultado e caixa juntos explicam o lucro que não aparece na conta.'),
  dict(type='recap', t='green', kick='Resumo', title='Com o cliente:', items=['DRE: teve resultado?', 'DFC: para onde foi o caixa?', 'Os dois, juntos'], fs=52),
  dict(type='cta', t='dark', kick='Salve', title='Salve para explicar ao seu cliente.'),
 ],
}
# cover for 'dark' theme needs mark style on dark
async def main(only=None, outroot=R, scratch=False):
    alts={}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width':1080,'height':1350})
        for name, slides in POSTS.items():
            if only and name not in only: continue
            d = f'{outroot}/{name}'; os.makedirs(d, exist_ok=True)
            n=len(slides); alts[name]=[]
            for i,s in enumerate(slides):
                await pg.set_content(build(s,i,n)); await pg.wait_for_timeout(250)
                await pg.screenshot(path=f'{d}/slide{i+1}.png')
                alts[name].append(alt(s,i,n))
        await b.close()
    json.dump(alts, open('/home/claude/gen21/alt.json','w'), ensure_ascii=False, indent=1)
if __name__=='__main__':
    only = sys.argv[1:] or None
    asyncio.run(main(only))
