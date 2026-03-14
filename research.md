---
layout: default
title: "Research"
permalink: /research/
---

<div class="page-header">
  <h1>Research</h1>
  <p class="subtitle">{{ site.data.research.subtitle }}</p>
  <p style="margin-top:0.5rem;font-size:0.9rem">
    <a href="{{ site.data.research.google_scholar }}" target="_blank" rel="noopener noreferrer">
      <i class="fas fa-graduation-cap" aria-hidden="true"></i> Google Scholar
    </a>
  </p>
</div>

## Research Position

<div class="research-entry">
  <h3>{{ site.data.research.position.title }}</h3>
  <p class="research-meta">
    <span class="research-role">{{ site.data.research.position.role }}</span> &mdash; {{ site.data.research.position.lab }}, {{ site.data.research.position.institution }}
  </p>
  <p>{{ site.data.research.position.description }}</p>
  <p><strong>My work has focused on:</strong></p>
  <ul>
    {% for item in site.data.research.position.focus %}
    <li>
      <strong>{{ item.title }}</strong> — {{ item.detail }}
    </li>
    {% endfor %}
  </ul>
  <p style="font-size:0.875rem;color:var(--color-text-muted)">
    {{ site.data.research.position.note }}
  </p>
</div>

---

## Publications

{% for pub in site.data.research.publications %}
<div class="publication">
  <p class="publication-title">{{ pub.title }}</p>
  <p class="publication-authors">{{ pub.authors }}</p>
  <p class="publication-venue">{{ pub.venue }}</p>
  <p style="font-size:0.9rem;margin-top:0.5rem">{{ pub.description }}</p>
  <div class="tags" style="margin-top:0.5rem">
    {% for tag in pub.tags %}
    <span class="tag">{{ tag }}</span>
    {% endfor %}
  </div>
</div>
{% endfor %}

---

## Research Interests

<ul>
{% for interest in site.data.research.interests %}
  <li><strong>{{ interest | split: " — " | first }}</strong> — {{ interest | split: " — " | last }}</li>
{% endfor %}
</ul>
