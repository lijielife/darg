#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver
from shareholder.models import Shareholder, Position, OptionTransaction
from shareholder.tasks import update_order_cache_task


@receiver(models.signals.post_save, sender=Position)
@receiver(models.signals.post_save, sender=OptionTransaction)
@receiver(models.signals.post_save, sender=Shareholder)
def update_order_cache(sender, instance, created, **kwargs):
    if sender == Shareholder:
        update_order_cache_task.apply_async([instance.pk])
    if sender == Position and instance.buyer:
        update_order_cache_task.apply_async([instance.pk])
    if sender == Position and instance.seller:
        update_order_cache_task.apply_async([instance.pk])
    if sender == OptionTransaction and instance.buyer:
        update_order_cache_task.apply_async([instance.pk])
    if sender == OptionTransaction and instance.seller:
        update_order_cache_task.apply_async([instance.pk])
