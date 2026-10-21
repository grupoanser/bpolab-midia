import asyncio, base64
from playwright.async_api import async_playwright
sim = base64.b64encode(open('sim.png','rb').read()).decode()
simw = base64.b64encode(open('sim_white.png','rb').read()).decode()
G='#A1D141'; K='#111111'
slides = [
 dict(bg='#FFFFFF', fg=K, kicker='BPO.Lab', title='BPO financeiro<br>x contabilidade', sub='Qual é a diferença para quem quer trabalhar na área?', big=True, tsize=98),
 dict(bg='#F6F6F2', fg=K, kicker='CONTABILIDADE', title='O foco é a parte legal e fiscal', body='Impostos, obrigações e registros contábeis.'),
 dict(bg='#F6F6F2', fg=K, kicker='BPO FINANCEIRO', title='O foco é a rotina e a gestão financeira do cliente', body='Contas, conciliação, fluxo de caixa e análise de resultado.'),
 dict(bg=G, fg=K, kicker='RESUMINDO', title='A contabilidade olha para a obrigação. O BPO olha para o caixa e para o resultado.'),
 dict(bg='#F6F6F2', fg=K, kicker='UM SUBSTITUI O OUTRO?', title='Não.', body='Quem entende <b>os dois lados</b> entende melhor o cliente.'),
 dict(bg=K, fg='#FFFFFF', kicker='E VOCÊ?', title='Você já trabalha ou quer trabalhar com BPO?', body='Comenta aqui e segue <b style="color:%s">@bpo.lab</b>' % G, dark=True),
]
def html(s,i):
    logo_filter = ''
    big = s.get('big')
    tsize = s.get('tsize', 118 if big else 76)
    body = ''
    if s.get('body'): body = f'<p class="body">{s["body"]}</p>'
    if s.get('sub'): body = f'<p class="body sub">{s["sub"]}</p>'
    accent = '' if big else f'<div class="bar"></div>'
    return f'''<html><head><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:{s['bg']};color:{s['fg']};font-family:Poppins,Inter,sans-serif;position:relative;overflow:hidden}}
.wrap{{position:absolute;left:90px;right:90px;top:170px;bottom:170px;display:flex;flex-direction:column;justify-content:center}}
.kicker{{font-weight:700;font-size:38px;letter-spacing:2px;margin-bottom:34px;color:{'#111' if big else ('#fff' if s.get('dark') else '#111')}}}
.kicker span{{background:{G};color:#111;padding:6px 22px;border-radius:40px}}
h1{{font-weight:800;font-size:{tsize}px;line-height:1.08;letter-spacing:-1px}}
.bar{{width:120px;height:14px;border-radius:10px;background:{G};margin:40px 0}}
.body{{font-size:46px;line-height:1.35;font-weight:400;margin-top:{'44px' if big else '0'}}}
.body b{{font-weight:700}}
.sub{{font-weight:600}}
.logo{{position:absolute;left:90px;top:70px;width:84px;{logo_filter}}}
.page{{position:absolute;right:90px;top:92px;font-size:30px;font-weight:600;opacity:.6}}
.foot{{position:absolute;left:90px;bottom:70px;font-size:30px;font-weight:600;opacity:.7}}
</style></head><body>
<img class="logo" src="data:image/png;base64,{simw if s.get('dark') else sim}">
<div class="page">{i+1}/{len(slides)}</div>
<div class="wrap"><div class="kicker"><span>{s['kicker']}</span></div><h1>{s['title']}</h1>{accent}{body}</div>
<div class="foot">@bpo.lab</div>
</body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium') if False else await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1080,'height':1350})
        for i,s in enumerate(slides):
            await pg.set_content(html(s,i)); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'slide{i+1}.png')
        await b.close()
asyncio.run(main())
