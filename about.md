---
layout: default
title: "About"
permalink: /about/
---

<div class="page-header">
  <h1>About</h1>
  <p class="subtitle">Computer Science student at Cornell University.</p>
</div>

{{ site.data.about.bio | markdownify }}

## Interests

<ul>
{% for interest in site.data.about.interests %}
  <li><strong>{{ interest | split: " — " | first }}</strong> — {{ interest | split: " — " | last }}</li>
{% endfor %}
</ul>

## Education

**{{ site.data.about.education.institution }}** — {{ site.data.about.education.degree }}
*Expected {{ site.data.about.education.expected }}* | GPA: {{ site.data.about.education.gpa }}

Relevant coursework:
{% for course in site.data.about.education.coursework %}
- {{ course }}
{% endfor %}

## Skills

**Programming:** {{ site.data.about.skills.programming }}

**Machine Learning:** {{ site.data.about.skills.machine_learning }}

**Tools:** {{ site.data.about.skills.tools }}

## Contact

- **Email:** [{{ site.data.profile.email }}](mailto:{{ site.data.profile.email }})
- **LinkedIn:** [linkedin.com/in/rmy43]({{ site.data.profile.social.linkedin }})
- **GitHub:** [github.com/ryanmye]({{ site.data.profile.social.github }})
