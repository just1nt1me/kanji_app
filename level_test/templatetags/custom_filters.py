from django import template

register = template.Library()

@register.filter(name='filter_level')
def filter_level(results, level):
    return [result for result in results if result[0].level == level]
