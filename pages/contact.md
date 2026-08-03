---
layout: default
permalink: /contact/
title: Напишіть мені щось
---

<div class="container">
  <div class="page-content">
    <h1 class="page-title">Напишіть мені щось</h1>

    <div class="contact-intro">{% capture contact_text %}{% include content/contact-text.md %}{% endcapture %}{{ contact_text | markdownify }}</div>

    <div>
      <a href="mailto:online.writing.page@gmail.com" class="contact-link">
        <img src="{{ '/assets/images/site/email-icon.png' | relative_url }}" class="btn-icon" alt="">
        Електронна пошта
      </a>
    </div>
  </div>
</div>
