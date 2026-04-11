---
layout: default
title: "About"
permalink: /about/
description: "About Ryan Ye — undergraduate in Computer Science at Cornell University, researching machine learning and computer vision."
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

- **Email:** [{{ site.email }}](mailto:{{ site.email }})
- **LinkedIn:** [linkedin.com/in/{{ site.linkedin_username }}](https://linkedin.com/in/{{ site.linkedin_username }})
- **GitHub:** [github.com/{{ site.github_username }}](https://github.com/{{ site.github_username }})
