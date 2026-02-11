---
layout: page
title: Inner Musings
permalink: /blog/
---

<div>
  {% for post in site.posts %}
    {% if post.categories contains "booknotes" %}
    {% else %}
      <div class="blog-list-row">
        <span class="blog-list-date">{{ post.date | date: "%b %Y" }}</span>
        <span class="blog-list-title"><a href="{{ post.url }}">{{ post.title }}</a></span>
      </div>
    {% endif %}
  {% endfor %}
</div>

<div class="subscription-section">
  <div class="subscription-title">Get these directly in your inbox</div>
  <div class="subscription-description">
    Thoughts on building companies, AI × Commerce, and startup lessons from someone who's scaled companies beyond $100M+.
  </div>
  <a href="https://rhythm.substack.com" class="subscription-button" target="_blank">Subscribe</a>
</div>