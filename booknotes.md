---
layout: page
title: Book Notes
permalink: /book-notes/
---


<div class="posts">
  {% for post in site.posts %}

    {% if post.categories contains "booknotes" %}
    <article class="post">
    {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
    <span class="post-meta">{{ post.date | date: date_format }}</span>
      <h2><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h2>
    </article>
    {% endif %}
  {% endfor %}
</div>
