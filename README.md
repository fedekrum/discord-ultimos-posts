# Últimos posts del foro (Discord)

Actualiza cada 5 minutos un mensaje en `#ultimos-posts` con los 10 posts más
recientes de los canales foro del servidor Interlink Network Comunidad.

## Cómo funciona

- GitHub Actions ejecuta `ultimos_posts.py` con un cron `*/5 * * * *` (UTC).
- El script consulta los hilos activos de los foros, los ordena por fecha y
  edita el último mensaje del bot en el canal. No guarda estado en disco, así
  que funciona aunque cada corrida use una máquina distinta.
- El token del bot se guarda como secreto `DISCORD_TOKEN` del repositorio.

## Mantimiento

Los workflows programados se desactivan automáticamente después de 60 días sin
actividad en el repositorio. Para evitarlo, hacé un commit (o ejecutá el
workflow a mano con `workflow_dispatch`) al menos una vez cada dos meses.

## Ejecutar a mano

En la pestaña **Actions** del repositorio, elegí el workflow
**Últimos posts del foro** y presioná **Run workflow**.
