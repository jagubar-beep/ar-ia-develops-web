"""Dependency-free static catalog. Run after editing apps.json; commit generated HTML."""
import json, re
from html import escape
from pathlib import Path

ROOT=Path(__file__).resolve().parent
APPS=json.loads((ROOT/'apps.json').read_text(encoding='utf-8'))
STATUSES={'concept','evaluation','development','internal','closed','published','maintenance'}
def e(value):return escape(str(value),quote=True)
def head(title,description,path):
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(description)}"><title>{e(title)}</title>
<link rel="canonical" href="https://jagubar-beep.github.io/ar-ia-develops-web/{path}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%2309131c'/%3E%3Cpath d='M7 24L16 7l9 17M11 18h10' fill='none' stroke='%2364e0cd' stroke-width='3'/%3E%3C/svg%3E">
<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="catalog.css"></head><body>
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="wrap"><a class="brand" href="index.html" aria-label="AR-IA DevelOps, inicio">AR-IA<span>DevelOps</span></a>
<nav aria-label="Principal"><a href="index.html#aplicaciones">Aplicaciones</a><a href="index.html#frontear">FronteAR</a><a href="index.html#librarium">Librarium</a><a href="index.html#estudio">Estudio</a><a href="index.html#contacto">Contacto</a><a href="privacidad.html">Privacidad</a></nav></header>'''
FOOTER='''<footer class="wrap"><span>AR-IA DevelOps · Proyecto de Juan Luis Agüera Barasona</span><span>Hecho para explorar. <a href="privacidad.html">Privacidad</a></span></footer></body></html>'''
def project(app,detail=False):
    features=''.join(f'<li><span>{e(f["label"])}</span> {e(f["text"])}</li>' for f in app['features'])
    version=f'<p class="small">{e(app.get("versionLabel","Versión"))}: {e(app["version"])}</p>' if app['version'] else ''
    links=f'<a class="text-link" href="{e(app["privacyUrl"])}">Privacidad de {e(app["name"])} <span aria-hidden="true">↗</span></a>'
    if not detail:links=f'<a class="text-link" href="{e(app["id"])}.html">Conoce {e(app["name"])} <span aria-hidden="true">↗</span></a> · '+links
    if app['playStoreUrl']:links+=f' · <a class="text-link" href="{e(app["playStoreUrl"])}">Google Play</a>'
    if app['repositoryUrl']:links+=f' · <a class="text-link" href="{e(app["repositoryUrl"])}">Código público</a>'
    heading='h1' if detail else 'h2'
    return f'''<section id="{e(app['id'])}" class="project wrap {e(app['id'])}" aria-labelledby="{e(app['id'])}-title">
<div class="art"><img src="{e(app['icon'])}" alt="{e(app['iconAlt'])}" width="1024" height="1024" {'loading="lazy"' if not detail else ''}></div>
<div class="project-copy"><p class="eyebrow">{e(app['eyebrow'])}</p><div class="title-row"><{heading} id="{e(app['id'])}-title">{e(app['name'])}</{heading}><span class="badge">{e(app['statusLabel'])}</span></div>
<p class="lead">{e(app['tagline'])}</p><p>{e(app['description'])}</p><ul class="features">{features}</ul>
<p class="availability">{e(app['availability'])}</p>{version}<p>{links}</p><p class="small">{e(app['notice'])}</p></div></section>'''
def gallery(app):
    if not app['screenshots']:return ''
    pictures=''.join(f'<figure><a href="{e(s["src"])}"><img src="{e(s["src"])}" alt="{e(s["alt"])}" width="720" height="1604" loading="lazy"></a><figcaption>{e(s["caption"])}</figcaption></figure>' for s in app['screenshots'])
    return f'<section class="wrap gallery-section" aria-label="Capturas de {e(app["name"])}"><h2>Un vistazo a {e(app["name"])}</h2><p class="small">Pantallas reales con datos ficticios. Pulsa una captura para ampliarla.</p><div class="gallery">{pictures}</div></section>'
def build():
    ids=set()
    for app in APPS:
        assert re.fullmatch('[a-z][a-z0-9-]*',app['id']) and app['id'] not in ids
        ids.add(app['id']);assert app['status'] in STATUSES
        assert app['playStoreUrl'] is None or app['playStoreUrl'].startswith('https://play.google.com/store/apps/details?id=')
        # Private repositories must never be added to this public catalog.
        assert app['repositoryUrl'] is None or app.get('repositoryPublic') is True
        assert (ROOT/app['icon']).is_file() and (ROOT/app['privacyUrl']).is_file()
        for s in app['screenshots']:assert (ROOT/s['src']).is_file()
        history=''.join(f'<li>{e(item)}</li>' for item in app['roadmapHighlights'])
        news=f'<section class="wrap news"><h2>Últimos avances</h2><ul>{history}</ul></section>' if history else ''
        (ROOT/f'{app["id"]}.html').write_text(head(f'{app["name"]} — AR-IA DevelOps',app['description'],f'{app["id"]}.html')+'<main id="contenido">'+project(app,True)+gallery(app)+news+'<p class="wrap back-link"><a href="index.html#aplicaciones">Volver a las aplicaciones</a></p></main>'+FOOTER,encoding='utf-8')
    home=head('AR-IA DevelOps — Aplicaciones con otra mirada','Estudio independiente de aplicaciones Android. Descubre FronteAR y Librarium: territorio, lecturas y nuevas formas de explorar.','')
    home+='''<main id="contenido"><section class="hero wrap"><p class="eyebrow">ESTUDIO INDEPENDIENTE · APLICACIONES ANDROID</p><h1>Otra forma de mirar.<br><em>Más historias por descubrir.</em></h1><div class="intro"><p>Creamos herramientas que acercan la tecnología a lo que importa: el territorio que recorres y las historias que guardas. Dos aplicaciones, una misma curiosidad.</p><a class="button" href="#aplicaciones">Explora las aplicaciones <span aria-hidden="true">↘</span></a></div></section>
<section id="aplicaciones" class="wrap catalog-heading"><p class="eyebrow">NUESTRO CATÁLOGO</p><h2>Ideas que toman forma.</h2><p>Conoce cada proyecto y su disponibilidad actual.</p></section>'''
    home+=''.join(project(app) for app in APPS)
    home+='''<section id="estudio" class="wrap about"><p class="eyebrow">SOBRE EL ESTUDIO</p><h2>Tecnología cercana.<br>Curiosidad sin fronteras.</h2><p>AR-IA DevelOps es un estudio independiente de aplicaciones Android. Diseñamos experiencias claras, útiles y con identidad propia, y las mejoramos paso a paso con la ayuda de quienes las prueban.</p></section>
<section id="contacto" class="contact wrap"><div><p class="eyebrow">HABLEMOS</p><h2>Las buenas ideas<br>empiezan conversando.</h2></div><div><p>Consultas sobre el estudio, sus aplicaciones o las pruebas:</p><a class="email" href="mailto:abjuanlu@gmail.com">abjuanlu@gmail.com</a><p class="small">No envíes contraseñas, documentos de identidad ni ubicaciones privadas innecesarias.</p></div></section></main>'''
    (ROOT/'index.html').write_text(home+FOOTER,encoding='utf-8')
if __name__=='__main__':build()
