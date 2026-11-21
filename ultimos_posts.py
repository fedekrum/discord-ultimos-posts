"""Publica/actualiza un mensaje con los 10 posts más recientes de los foros.

Se ejecuta una sola vez por corrida (ideal para GitHub Actions). El estado no
se guarda en disco: busca el último mensaje del bot en el canal y lo edita.
"""

import json
import os
import urllib.error
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.environ['DISCORD_TOKEN']
GUILD = '1573344030853562449'
CHANNEL = '1573489681956606062'
BOT_ID = '1573372104953438308'
BASE = 'https://discord.com/api/v10'
TZ = ZoneInfo('America/Argentina/Buenos_Aires')


def req(method, path, body=None):
    headers = {
        'Authorization': 'Bot ' + TOKEN,
        'User-Agent': 'DiscordBot (https://discord.com, 1.0)',
    }
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode()
        headers['Content-Type'] = 'application/json'
    request = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        raw = response.read()
        return json.loads(raw) if raw else None


def esc(texto):
    for c in ('\\', '*', '_', '`', '[', ']', '~', '>'):
        texto = texto.replace(c, '\\' + c)
    return texto


def build():
    channels = req('GET', f'/guilds/{GUILD}/channels')
    forums = {c['id']: c['name'] for c in channels if c['type'] == 15}
    data = req('GET', f'/guilds/{GUILD}/threads/active')
    threads = data['threads'] if isinstance(data, dict) else data
    posts = [t for t in threads if t.get('parent_id') in forums]
    posts.sort(key=lambda t: t.get('thread_metadata', {}).get('create_time') or '', reverse=True)
    posts = posts[:10]

    lines = ['**Últimos posts del foro** (se actualiza automáticamente)', '']
    if not posts:
        lines.append('_Todavía no hay posts en los foros._')
    else:
        for i, t in enumerate(posts, 1):
            dt = datetime.fromisoformat(
                t['thread_metadata']['create_time'].replace('Z', '+00:00')).astimezone(TZ)
            ts = dt.strftime('%d/%m %H:%M')
            lines.append(
                f'{i}. [{esc(t["name"])}](https://discord.com/channels/{GUILD}/{t["id"]})'
                f' — `{forums[t["parent_id"]]}` — {ts}')
    lines += ['', f'_Actualizado: {datetime.now(TZ).strftime("%d/%m/%Y %H:%M")}_']
    return '\n'.join(lines)


def main():
    content = build()
    messages = req('GET', f'/channels/{CHANNEL}/messages?limit=100')
    own = next((m for m in messages if m.get('author', {}).get('id') == BOT_ID), None)
    if own:
        req('PATCH', f'/channels/{CHANNEL}/messages/{own["id"]}', {'content': content})
        print('Mensaje actualizado')
    else:
        req('POST', f'/channels/{CHANNEL}/messages', {'content': content})
        print('Mensaje creado')


if __name__ == '__main__':
    main()
