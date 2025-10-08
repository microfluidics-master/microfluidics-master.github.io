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
    <textarea name="message" rows="10" cols="40" required></textarea>
  </label>
  
  <!-- Honeypot (anti-spam) -->
  <input type="text" name="_gotcha" style="display:none">
  <!-- Redirect after submit -->
  
  <input type="hidden" name="_redirect" value="https://microfluidics-master.github.io">
  
  <button type="submit">Send</button>
</form>