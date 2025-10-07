---
title: "Contact"
layout: page
permalink: /contact/
---

<form action="https://formspree.io/f/xeorlejk" method="POST">
  <label>Your email
    <input type="email" name="email" required>
  </label>
  <label>Message
    <textarea name="message" rows="6" required></textarea>
  </label>
  <!-- Honeypot (anti-spam) -->
  <input type="text" name="_gotcha" style="display:none">
  <!-- Redirect after submit -->
  <input type="hidden" name="_redirect" value="https://your-domain.github.io/thanks/">
  <button type="submit">Send</button>
</form>