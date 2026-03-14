---
layout: default
title: "About"
---

<div class="profile-section">
  <div class="profile-left">
    <div class="profile-avatar">RY</div>
    <h1 class="profile-name">Ryan Ye</h1>
    <p class="profile-position">
      Computer Science<br>
      <a href="https://www.cs.cornell.edu/" target="_blank" rel="noopener noreferrer">Cornell University</a>
    </p>
    <div class="profile-social">
      <a href="mailto:rmy43@cornell.edu" title="Email"><i class="fas fa-envelope"></i></a>
      <a href="https://github.com/matthewj5" target="_blank" rel="noopener noreferrer" title="GitHub"><i class="fab fa-github"></i></a>
      <a href="https://www.linkedin.com/in/rmy43/" target="_blank" rel="noopener noreferrer" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
    </div>
  </div>

  <div class="profile-right">
    <p>
      Computer Science student at Cornell University interested in machine learning,
      computer vision, and AI for scientific discovery. I enjoy working at the intersection
      of AI and real-world systems, particularly in domains where better data and automation
      can help researchers scale their work.
    </p>
    <p>
      Currently, I conduct research in the Sun Lab at Cornell, where I work on computer
      vision methods for animal behavior monitoring in agricultural environments.
    </p>
    <div class="profile-contact-row">
      <span><i class="fas fa-envelope fa-sm"></i> <a href="mailto:rmy43@cornell.edu">rmy43@cornell.edu</a></span>
      <span><i class="fab fa-linkedin fa-sm"></i> <a href="https://www.linkedin.com/in/rmy43/" target="_blank" rel="noopener noreferrer">linkedin.com/in/rmy43</a></span>
      <span><i class="fab fa-github fa-sm"></i> <a href="https://github.com/matthewj5" target="_blank" rel="noopener noreferrer">github.com/matthewj5</a></span>
    </div>
    <p class="spotify-widget">
      <i class="fab fa-spotify" style="color:#1DB954"></i>
      <span id="spotify-now-playing">Loading&hellip;</span>
    </p>
  </div>
</div>

<div class="content-section">
  <h2 class="section-title">About</h2>

  <p>
    I am an undergraduate studying Computer Science at Cornell University (College of
    Engineering). My interests lie broadly in:
  </p>
  <ul>
    <li>Machine learning and computer vision</li>
    <li>AI for science and real-world systems</li>
    <li>Representation learning and foundation models</li>
    <li>Data-efficient learning methods</li>
  </ul>
  <p>
    I enjoy collaborating across disciplines and working with researchers in domains like
    veterinary science, agriculture, and economics to design AI systems that help analyze
    complex real-world data.
  </p>
  <p>
    Outside of academics, I am a violinist in the Cornell Orchestras and enjoy exploring
    how technology and creativity intersect.
  </p>
</div>

<div class="content-section">
  <div class="section-header">
    <h2 class="section-title" style="border:none;padding:0;margin:0">Research</h2>
    <a href="{{ '/research' | relative_url }}">see more &rarr;</a>
  </div>

  <div class="research-entry">
    <h3>AI for Animal Behavior Monitoring</h3>
    <p class="research-meta">
      <span class="research-role">Undergraduate Researcher</span> &mdash; Sun Lab, Cornell University
    </p>
    <p>
      I work on scalable computer vision systems for analyzing dairy calf behavior in
      agricultural environments, supporting veterinary researchers studying early indicators
      of disease and welfare. Work spans pose classification with self-supervised DINO
      features, YOLO-based object detection on a self-annotated dataset, and evaluation
      of vision-language models for farm settings.
    </p>
    <p style="font-size:0.875rem;color:var(--color-text-muted)">
      Conducted as part of the Bowers Undergraduate Research Experience (BURE) with
      support from a CIDA grant.
    </p>
  </div>
</div>

<div class="content-section">
  <div class="section-header">
    <h2 class="section-title" style="border:none;padding:0;margin:0">Recent Posts</h2>
    <a href="{{ '/blog' | relative_url }}">all posts &rarr;</a>
  </div>

  <ul class="post-list" role="list">
    {% assign recent_posts = site.posts | limit: 3 %}
    {% for post in recent_posts %}
    <li class="post-item">
      <h3 class="post-item-title">
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </h3>
      <p class="post-item-meta">
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
        {% if post.tags and post.tags.size > 0 %}
        &mdash;
        {% for tag in post.tags %}<span class="tag">{{ tag }}</span> {% endfor %}
        {% endif %}
      </p>
      {% if post.excerpt %}
      <p class="post-item-excerpt">{{ post.excerpt | strip_html | truncate: 160 }}</p>
      {% endif %}
    </li>
    {% else %}
    <li class="post-item">
      <p class="post-item-excerpt">No posts yet — check back soon!</p>
    </li>
    {% endfor %}
  </ul>
</div>

<script>
(function () {
  function timeAgo(isoStr) {
    var played = new Date(isoStr);
    var now    = new Date();
    var secs   = Math.floor((now - played) / 1000);
    if (secs < 60)  return secs + ' second' + (secs === 1 ? '' : 's') + ' ago';
    var mins = Math.floor(secs / 60);
    if (mins < 60)  return mins + ' minute' + (mins === 1 ? '' : 's') + ' ago';
    var hrs  = Math.floor(mins / 60);
    if (hrs  < 24)  return hrs  + ' hour'   + (hrs  === 1 ? '' : 's') + ' ago';
    var days = Math.floor(hrs  / 24);
    return days + ' day' + (days === 1 ? '' : 's') + ' ago';
  }

  var el = document.getElementById('spotify-now-playing');
  if (!el) return;

  fetch('{{ "/assets/data/now-playing.json" | relative_url }}?t=' + Date.now())
    .then(function (r) { return r.json(); })
    .then(function (data) {
      if (!data.track) {
        el.textContent = 'No recent tracks.';
        return;
      }
      var t = data.track;
      var artistLinks = t.artists.map(function (a) {
        return '<a href="' + a.url + '" target="_blank" rel="noopener noreferrer">' +
               escapeHtml(a.name) + '</a>';
      }).join(', ');
      el.innerHTML =
        'listened to <a href="' + t.url + '" target="_blank" rel="noopener noreferrer">' +
        escapeHtml(t.name) + '</a> by ' + artistLinks +
        ' <span class="spotify-time">(' + timeAgo(t.played_at) + ')</span>';
    })
    .catch(function () {
      el.textContent = 'Could not load recent track.';
    });

  function escapeHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
              .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
})();
</script>
