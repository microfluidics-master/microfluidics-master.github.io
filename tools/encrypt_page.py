#!/usr/bin/env python3
"""Password-protect a page of the static site (client-side AES-GCM encryption).

Usage:
    pip install cryptography
    python3 tools/encrypt_page.py _private/calendar-content.html calendar.md "the-password"

The plaintext source lives in _private/ (git-ignored, never pushed). Only the encrypted
blob is committed; the browser decrypts it with the Web Crypto API once the password is typed.
Re-run this script to change the password or update the content.
"""
import base64, os, sys, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 600_000

def main(src, dst, password):
    plaintext = open(src, encoding="utf-8").read().encode()
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(password.encode())
    ct = AESGCM(key).encrypt(iv, plaintext, None)
    b64 = lambda b: base64.b64encode(b).decode()
    payload = json.dumps({"salt": b64(salt), "iv": b64(iv), "ct": b64(ct), "iter": ITER})
    page = f"""---
title: Schedule (students)
layout: page
permalink: /calendar/
hide_title: true
sitemap: false
noindex: true
redirect_from:
  - /schedule/
---

<div id="protected-area" class="protected">
  <form id="pw-form" class="pw-form" autocomplete="off">
    <h2>Espace étudiant·e·s / Students only</h2>
    <p>L'emploi du temps est réservé aux étudiant·e·s inscrit·e·s.<br>
       The schedule is restricted to enrolled students.</p>
    <input id="pw" type="password" placeholder="Mot de passe / Password" aria-label="Password" required>
    <label class="pw-remember"><input id="pw-keep" type="checkbox" checked> Se souvenir sur cet appareil / Remember on this device</label>
    <button type="submit" class="btn">Accéder / Enter</button>
    <p id="pw-error" class="pw-error" hidden>Mot de passe incorrect / Wrong password</p>
  </form>
</div>

<script>
(function () {{
  const P = {payload};
  const d = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
  async function decrypt(pw) {{
    const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey({{name: 'PBKDF2', salt: d(P.salt), iterations: P.iter, hash: 'SHA-256'}},
      base, {{name: 'AES-GCM', length: 256}}, false, ['decrypt']);
    const pt = await crypto.subtle.decrypt({{name: 'AES-GCM', iv: d(P.iv)}}, key, d(P.ct));
    return new TextDecoder().decode(pt);
  }}
  async function unlock(pw, keep) {{
    try {{
      const html = await decrypt(pw);
      document.getElementById('protected-area').innerHTML = html;
      try {{ if (keep) localStorage.setItem('mm-cal-pw', pw); }} catch (e) {{}}
      return true;
    }} catch (e) {{ return false; }}
  }}
  let saved = null; try {{ saved = localStorage.getItem('mm-cal-pw'); }} catch (e) {{}}
  if (saved) unlock(saved, false).then(ok => {{ if (!ok) try {{ localStorage.removeItem('mm-cal-pw'); }} catch (e) {{}} }});
  document.getElementById('pw-form').addEventListener('submit', async ev => {{
    ev.preventDefault();
    const ok = await unlock(document.getElementById('pw').value, document.getElementById('pw-keep').checked);
    document.getElementById('pw-error').hidden = ok;
  }});
}})();
</script>
"""
    open(dst, "w", encoding="utf-8").write(page)
    print(f"Encrypted {src} -> {dst}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
