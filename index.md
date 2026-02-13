---
layout: home
title: "Welcome to My Blog"
subtitle: "Thoughts on Technology, Programming, and Life"
---

# Hello, I'm Chris 👋

Welcome to my personal blog! I write about:
- Software development
- AI and machine learning
- Web technologies
- Personal projects
- Random thoughts

## Recent Posts

{% for post in site.posts limit:5 %}
### [{{ post.title }}]({{ post.url | relative_url }})
{{ post.date | date: "%Y-%m-%d" }} · {{ post.excerpt | strip_html | truncate: 150 }}
{% endfor %}

[View all posts →](/archive)