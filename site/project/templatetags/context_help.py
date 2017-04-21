#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.inclusion_tag('_context_help.html')
def context_help(text):
    return {'text': text}
