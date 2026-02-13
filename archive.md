---
layout: page
title: "文章归档"
---

# 文章归档

按年份查看所有文章：

{% assign postsByYear = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
{% for year in postsByYear %}
<div class="archive-year">{{ year.name }}年</div>
<ul class="archive-list">
  {% for post in year.items %}
  <li class="archive-post">
    <span class="archive-date">{{ post.date | date: "%m月%d日" }}</span>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>
{% endfor %}

{% if site.posts.size == 0 %}
<p>还没有文章，敬请期待！</p>
{% endif %}