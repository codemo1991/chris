---
layout: page
title: "标签"
---

# 标签

{% assign tags = site.tags | sort %}
{% if tags.size > 0 %}
<div class="tag-cloud">
  {% for tag in tags %}
    {% assign tag_name = tag[0] %}
    {% assign tag_count = tag[1].size %}
    <a href="/tags/{{ tag_name | slugify }}" class="tag-link">
      {{ tag_name }} ({{ tag_count }})
    </a>
  {% endfor %}
</div>
{% else %}
<p>还没有标签，敬请期待！</p>
{% endif %}

## 按标签查看文章

{% for tag in tags %}
{% assign tag_name = tag[0] %}
{% assign tag_posts = tag[1] %}

<h2 id="{{ tag_name | slugify }}">{{ tag_name }}</h2>
<ul>
  {% for post in tag_posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <span class="post-date">{{ post.date | date: "%Y年%m月%d日" }}</span>
  </li>
  {% endfor %}
</ul>
{% endfor %}