import re,subprocess,os
src=open('/tmp/carrossel3/gen.py').read()
a=src.index('slides = ['); b=src.index(']\ndef html')+1
G='#A1D141'; K='#111111'; W='#FFFFFF'; O='#F6F6F2'
def cta(txt,kicker='E VOCÊ?'): return dict(bg=K,fg=W,kicker=kicker,title=txt[0],body=txt[1]+' <b style="color:%s">@bpo.lab</b>'%G,dark=True)
posts={
'p2':[
 dict(bg=K,fg=W,kicker='BPO.Lab',title='3 mitos sobre<br>trabalhar com<br>BPO financeiro',sub='Você já ouviu algum deles?',big=True,dark=True,tsize=100),
 dict(bg=O,fg=K,kicker='MITO 1',title='“BPO é só lançar contas e fazer controle básico.”',body='<b>Na prática:</b> sem análise de resultado, é só financeiro operacional. Com análise, o cliente ganha clareza para <b>ter margem e crescer</b>.'),
 dict(bg=O,fg=K,kicker='MITO 2',title='“Para trabalhar com BPO, tem que ser contador.”',body='<b>Na prática:</b> contabilidade e BPO financeiro são <b>áreas diferentes</b>.'),
 dict(bg=O,fg=K,kicker='MITO 3',title='“Meu trabalho é só entregar tarefas.”',body='<b>Na prática:</b> o objetivo é o cliente ter <b>uma preocupação a menos</b>.'),
 dict(bg=G,fg=K,kicker='RESUMO',title='BPO vai além do controle básico, é diferente de contabilidade e existe para o cliente ter uma preocupação a menos.'),
 cta(('Qual desses mitos você já ouviu?','Comenta aqui e segue')),
],
'p4':[
 dict(bg=G,fg=K,kicker='BPO.Lab',title='Uma rotina típica de BPO financeiro',sub='Como é o trabalho na prática',big=True,tsize=100),
 dict(bg=O,fg=K,kicker='01',title='Conferir o que entrou e saiu',body='Extratos e lançamentos do dia.'),
 dict(bg=O,fg=K,kicker='02',title='Contas a pagar e a receber',body='Programar pagamentos e acompanhar os recebimentos.'),
 dict(bg=O,fg=K,kicker='03',title='Conciliação',body='Bater o banco com o sistema para os números fecharem.'),
 dict(bg=O,fg=K,kicker='04',title='Análise',body='Ler os resultados e apontar o que merece atenção do cliente.'),
 cta(('Quer detalhar algum desses passos?','Comenta aqui e segue')),
],
'p5':[
 dict(bg=K,fg=W,kicker='BPO.Lab',title='Glossário do BPO financeiro',sub='4 termos que você precisa conhecer',big=True,dark=True,tsize=100),
 dict(bg=O,fg=K,kicker='TERMO 1',title='Conciliação bancária',body='Comparar o extrato do banco com os lançamentos do sistema.'),
 dict(bg=O,fg=K,kicker='TERMO 2',title='Fluxo de caixa',body='O controle das entradas e saídas de dinheiro ao longo do tempo.'),
 dict(bg=O,fg=K,kicker='TERMO 3',title='DRE',body='Mostra receitas, custos e despesas de um período e se houve lucro ou prejuízo.'),
 dict(bg=O,fg=K,kicker='TERMO 4',title='Contas a pagar e a receber',body='O que a empresa deve pagar e o que ela vai receber.'),
 cta(('Qual termo você quer ver explicado a fundo?','Comenta aqui e segue'),'SALVE')
],
'p6':[
 dict(bg=W,fg=K,kicker='BPO.Lab',title='Qual a sua maior dúvida sobre BPO financeiro?',sub='Escolha uma ou escreva a sua',big=True,tsize=98),
 dict(bg=O,fg=K,kicker='DÚVIDA 1',title='Como começar na área?'),
 dict(bg=O,fg=K,kicker='DÚVIDA 2',title='O que estudar?'),
 dict(bg=O,fg=K,kicker='DÚVIDA 3',title='Quais ferramentas usar?'),
 dict(bg=O,fg=K,kicker='DÚVIDA 4',title='Como conseguir o primeiro cliente?'),
 cta(('Comenta a sua dúvida','As mais comuns viram conteúdo no'),'SUA VEZ'),
],
'p7':[
 dict(bg=G,fg=K,kicker='BPO.Lab',title='Dá para viver de BPO financeiro?',sub='A resposta curta: depende',big=True,tsize=104),
 dict(bg=O,fg=K,kicker='DEPENDE 1',title='Do que você entrega',body='Só a operação ou também a <b>análise de resultado</b>?'),
 dict(bg=O,fg=K,kicker='DEPENDE 2',title='De quantos clientes você atende bem',body='Qualidade na entrega sustenta o crescimento.'),
 dict(bg=O,fg=K,kicker='DEPENDE 3',title='De como você cobra pelo serviço',body='O valor precisa refletir o que você entrega.'),
 dict(bg=G,fg=K,kicker='RESUMO',title='Não é só entrar na área. É como você atua nela.'),
 cta(('Quer que eu detalhe cada ponto?','Comenta “quero” e segue'),'SUA VEZ'),
],
}
for k,sl in posts.items():
    os.makedirs(k,exist_ok=True)
    code=src[:a]+'slides = '+repr(sl)+src[b:]
    code=code.replace("path=f'slide{i+1}.png'","path=f'%s/slide{i+1}.png'"%k)
    open(f'gen_{k}.py','w').write(code)
    subprocess.run(['python3',f'gen_{k}.py'],check=True)
    from PIL import Image
    ims=[Image.open(f'{k}/slide{i}.png').resize((360,450)) for i in range(1,7)]
    c=Image.new('RGB',(1080,900),(120,120,120))
    for i,im in enumerate(ims): c.paste(im,((i%3)*360,(i//3)*450))
    c.save(f'{k}_contact.png')
