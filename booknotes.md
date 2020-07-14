---
layout: page
title: Book Notes
permalink: /book-notes/
---

<div class="posts">
  {% for post in site.booknotes %}
    <article class="post">

      <h1><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h1>

    </article>
  {% endfor %}
</div>
