---
layout: page
title: "Blog Archive"
permalink: /archive/
---

# Blog Archive

All posts in chronological order:

{% for post in site.posts %}
## [{{ post.title }}]({{ post.url | relative_url }})
{{ post.date | date: "%Y-%m-%d" }} · {{ post.excerpt | strip_html | truncate: 200 }}
{% endfor %}