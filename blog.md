---
layout: page
title: Inner Musings
permalink: /blog/
---

<style>
.blog-list-row {
  display: flex;
  align-items: baseline;
  margin-bottom: 0.7em;
}
.blog-list-date {
  color: #888;
  min-width: 90px;
  font-size: 1.05em;
  margin-right: 0.5em;
}
.blog-list-title a {
  color: #5B553A;
  text-decoration: none;
  font-size: 1.13em;
}
.blog-list-title a:hover {
  text-decoration: underline;
}
</style>

<div>
  {% for post in site.posts %}
    {% if post.categories contains "booknotes" %}
    {% else %}
      <div class="blog-list-row">
        <span class="blog-list-date">{{ post.date | date: "%b '%Y" }}</span>
        <span class="blog-list-title"><a href="{{ post.url }}">{{ post.title }}</a></span>
      </div>
    {% endif %}
  {% endfor %}
</div> 