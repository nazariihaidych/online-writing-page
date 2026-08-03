---
layout: default
permalink: /explanations/
title: Деякі пояснення
---

<div class="container">
  <div class="page-content">
    <h1 class="page-title">Деякі пояснення</h1>

    <div class="callout">{{ site.data.explanations.callout }}</div>

    <div class="toggle-list">
      {% for section in site.data.explanations.sections %}
      <div class="toggle-item">
        <details>
          <summary class="toggle-summary">
            <span class="toggle-arrow">▶</span>
            {{ section.title }}
          </summary>
          <div class="toggle-content">
            {{ section.content | markdownify }}
          </div>
        </details>
      </div>
      {% endfor %}
    </div>
  </div>
</div>
