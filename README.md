# AR-IA DevelOps — catálogo estático

Sitio existente: https://jagubar-beep.github.io/ar-ia-develops-web/

HTML/CSS sin dependencias, backend ni servicios de pago. GitHub Pages publica la raíz de main mediante el sistema existente (legacy Pages); no hay CNAME ni workflow propio. No cambiar DNS ni el método de publicación para actualizar el catálogo.

## Añadir o actualizar aplicaciones

1. Editar apps.json: id único, nombre, descripción, icono, capturas, plataforma, estado, versión opcional, características y enlaces oficiales. Un producto no anunciado no se añade al catálogo público.
2. Copiar solo recursos aprobados a assets/<id>. Las capturas deben ser reales y no contener datos personales.
3. Crear la política de privacidad de la nueva app y referenciarla en privacyUrl.
4. Ejecutar `python build.py` y `python check_site.py`. Se generan index.html y una página por app. No hace falta editar múltiples componentes ni ejecutar JavaScript en el visitante.
5. Revisar las páginas en móvil y escritorio; comprobar los enlaces externos modificados. Hacer commit/push de datos, assets, plantilla y HTML generado.
6. Publicar mediante avance fast-forward de main tras comprobaciones. Verificar el build de Pages y los contenidos visibles en la URL real. Si falla, revertir el commit publicado; no hacer reset/push forzado.

Estados: concept, evaluation, development, internal, closed, published, maintenance. statusLabel permite una descripción precisa: Librarium figura Pruebas internas · Por invitación tras verificar su release en Console. No poner un enlace interno de testers como descarga pública. playStoreUrl solo acepta fichas públicas; repositoryUrl requiere repositoryPublic=true y verificación real de que el código es público.

El respaldo previo está en backup/pre-librarium-2026-11-12. Se conserva index.html#frontear y privacidad-frontear.html; FronteAR mantiene sus textos y enlaces. La marca histórica AR-IA DevelOps permanece. No se cambia el repositorio Android de FronteAR ni su configuración en Play Console.

El correo público ya existente del estudio ha sido autorizado para Librarium. No incluir listas de testers, claves, builds Android ni documentación interna de Librarium en este repositorio público.
