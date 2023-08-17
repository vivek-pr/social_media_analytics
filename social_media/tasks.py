import re

from django.core.cache import cache

from social_media_analytics.celery import app
from .models import Post


@app.task
def analyze_post(post_id):
    cache_key = f'post_analysis_{post_id}'
    cached_result = cache.get(cache_key)

    if cached_result:
        return cached_result

    post = Post.objects.get(unique_id=post_id)
    content = post.content

    word_pattern = re.compile(r'\w+')
    word_count = 0
    total_characters = 0

    for match in word_pattern.finditer(content):
        word = match.group()
        word_count += 1
        total_characters += len(word)

    average_word_length = total_characters / word_count if word_count > 0 else 0

    analysis_result = {
        'word_count': word_count,
        'average_word_length': average_word_length
    }

    cache.set(cache_key, analysis_result, 3600)  # Cache the result for 1 hour

    return analysis_result

