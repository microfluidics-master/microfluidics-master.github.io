# Bilingual Jekyll (English + French)

Copy these folders/files into your existing repository to enable bilingual pages.

- `/en` and `/fr` with parallel pages
- `_includes/custom-head.html` + `_includes/lang-alt.html` + `_includes/lang-switch.html`
- `assets/css/style.scss` (imports Minima + small style)
- Root `index.html` redirect to `/en/`
- `_config.yml` with language defaults and remote_theme

After committing, your site should serve:
- English: /en/
- Français: /fr/
