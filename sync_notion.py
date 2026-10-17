#!/usr/bin/env python3
"""Lê o banco "Catálogo do site (estoque)" do Notion e gera plants.json e as fotos.
O que estiver vazio no Notion usa o texto padrão de base_plants.json."""
import os, io, json, re, unicodedata, urllib.request
from datetime import datetime, timezone, timedelta
try:
    from PIL import Image
    try:
        import pillow_heif; pillow_heif.register_heif_opener()
    except Exception:
        pass
except Exception:
    Image = None

ROOT = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(ROOT, 'fotos')

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def notion(path, body):
    req = urllib.request.Request('https://api.notion.com/v1' + path, data=json.dumps(body).encode(), method='POST',
        headers={'Authorization': 'Bearer ' + os.environ['NOTION_TOKEN'], 'Notion-Version': '2022-06-28', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def linhas():
    if os.environ.get('NOTION_FAKE'):
        return json.load(open(os.environ['NOTION_FAKE'], encoding='utf-8'))
    out, cur = [], None
    while True:
        body = {'page_size': 100, 'filter': {'property': 'Publicar', 'checkbox': {'equals': True}},
                'sorts': [{'property': 'Ordem', 'direction': 'ascending'}]}
        if cur:
            body['start_cursor'] = cur
        d = notion('/databases/%s/query' % os.environ['NOTION_DB_ID'], body)
        out += d['results']
        if not d.get('has_more'):
            return out
        cur = d['next_cursor']

def txt(p):
    if not p:
        return ''
    return ''.join(t.get('plain_text', '') for t in (p.get('title') or p.get('rich_text') or [])).strip()
def num(p): return p.get('number') if p else None
def chk(p): return bool(p and p.get('checkbox'))
def sel(p): return ((p or {}).get('select') or {}).get('name')
def arquivo(p):
    f = ((p or {}).get('files') or [None])[0]
    if not f:
        return None
    return (f.get('file') or f.get('external') or {}).get('url')

def baixar(url, destino):
    data = urllib.request.urlopen(url, timeout=60).read()
    if Image:
        im = Image.open(io.BytesIO(data)).convert('RGB')
        im.thumbnail((900, 900))
        im.save(destino, 'JPEG', quality=80, optimize=True)
    else:
        open(destino, 'wb').write(data)

def main():
    base = json.load(open(os.path.join(ROOT, 'base_plants.json'), encoding='utf-8'))
    meta_path = os.path.join(FOTOS, '.meta.json')
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    itens = []
    for pg in linhas():
        pr = pg['properties']
        nome = txt(pr.get('Planta'))
        if not nome:
            continue
        s = slug(nome)
        it = dict(base.get(s, {}))
        it['nome'] = nome
        for chave, campo in [('cat', 'Categoria')]:
            v = sel(pr.get(campo))
            if v: it[chave] = v
        it.setdefault('cat', 'Flores')
        for chave, campo in [('frase', 'Frase'), ('faixa', 'Faixa de preço'), ('sci', 'Nome científico'), ('sobre', 'Sobre'),
                             ('ben', 'Benefícios'), ('mist', 'Simbolismo e crenças'), ('luz', 'Luz'), ('agua', 'Água'),
                             ('dica', 'Dica de cuidado'), ('presente', 'Bom para presentear'), ('petTxt', 'Aviso de pets'), ('icone', 'Ícone')]:
            v = txt(pr.get(campo))
            if v: it[chave] = v
        v = num(pr.get('Preço'))
        if v is not None: it['preco'] = v
        v = num(pr.get('Ordem'))
        if v is not None: it['ordem'] = v
        it['estoque'] = num(pr.get('Estoque'))
        it['hoje'] = chk(pr.get('Disponível hoje'))
        it['pet'] = chk(pr.get('Tóxica para pets'))
        if it['pet'] and not it.get('petTxt'):
            it['petTxt'] = 'Tóxica se mastigada. Mantenha longe de pets e crianças.'
        if it['cat'] != 'Sob encomenda' and not (it.get('luz') or it.get('agua') or it.get('dica')):
            it['luz'], it['agua'], it['dica'] = 'Pergunte à Lyra.', 'Pergunte à Lyra.', 'Fale com a Lyra para receber as orientações de cuidado.'
        # foto
        url = arquivo(pr.get('Foto'))
        destino = os.path.join(FOTOS, s + '.jpg')
        editado = pg.get('last_edited_time', '')
        if url and (meta.get(s) != editado or not os.path.exists(destino)):
            os.makedirs(FOTOS, exist_ok=True)
            baixar(url, destino)
            meta[s] = editado
        if os.path.exists(destino):
            it['foto'] = 'fotos/%s.jpg' % s
        else:
            it['foto'] = 'fotos/placeholder.svg'
        it.setdefault('ordem', 999)
        itens.append(it)
    itens.sort(key=lambda i: i['ordem'])
    novo = {'p': [i for i in itens if i['cat'] != 'Sob encomenda'], 'e': [i for i in itens if i['cat'] == 'Sob encomenda']}
    caminho = os.path.join(ROOT, 'plants.json')
    antigo = json.load(open(caminho, encoding='utf-8')) if os.path.exists(caminho) else {}
    agora = datetime.now(timezone.utc)
    ultimo = antigo.get('atualizado')
    recente = False
    if ultimo:
        recente = agora - datetime.fromisoformat(ultimo.replace('Z', '+00:00')) < timedelta(days=20)
    if antigo.get('p') == novo['p'] and antigo.get('e') == novo['e'] and recente:
        print('Sem mudanças.')
    else:
        novo['atualizado'] = agora.isoformat().replace('+00:00', 'Z')
        json.dump(novo, open(caminho, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('plants.json atualizado: %d plantas, %d sob encomenda.' % (len(novo['p']), len(novo['e'])))
    json.dump(meta, open(meta_path, 'w'), indent=1) if os.path.isdir(FOTOS) else None

if __name__ == '__main__':
    main()
