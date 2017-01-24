#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import re

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from company.mixins import SubscriptionMixin
from utils.formatters import string_list_to_json


logger = logging.getLogger(__name__)


class FieldValidationMixin(object):

    def validate_number_segments(self, value):

        pattern = re.compile(r'[^0-9,\- ]')

        try:
            if isinstance(value, unicode):
                value = string_list_to_json(value)
        except ValueError:
            raise serializers.ValidationError(
                _("Invalid number segment. "
                  "Please use 1, 2, 3, 4-10.")
            )
            logger.warning("Invalid number segment: {}".format(value))

        for part in value:

            # validate value as we have to track value...
            if pattern.findall(str(part)):
                raise serializers.ValidationError(
                    _("Invalid number segment. "
                      "Please use 1, 2, 3, 4-10.")
                )
                logger.warning("Invalid number segment: {}".format(part))

            if isinstance(part, int):
                continue

            # --- VALIDATE u'X-Z' only
            # validate that start and end of u'1-9' are valid
            start, end = part.split('-')
            if int(start) >= int(end):
                raise serializers.ValidationError(
                    _("Number Segment Range start smaller/equal then end '{}'. "
                      "Please use 1, 2, 3, 4-10.".format(part))
                )
                logger.warning("Invalid number segment: {}".format(part))

        return value


class SubscriptionViewSetMixin(SubscriptionMixin):
    """
    mixin to handle subscription for viewsets
    """

    COMPANY_QUERY_VAR = 'company'
    subscription_features = []

    def get_user_companies(self):
        raise NotImplementedError(
            u'{} needs to implement get_user_companies'.format(self.__class__))

    def get_company_pks(self):
        """
        return a list of
        """
        company_qs = self.get_user_companies()

        q_cpks = self.request.query_params.getlist(self.COMPANY_QUERY_VAR)
        query_companies = map(int, [cpk for cpk in q_cpks if cpk.isdigit()])
        if query_companies:
            company_qs = company_qs.filter(pk__in=query_companies)

        company_pks = []
        for company in company_qs:
            if self.check_subscription(company, self.subscription_features):
                company_pks.append(company.pk)

        return company_pks


class SubscriptionSerializerMixin(object):
    """
    mixin to handle subscription for serializers
    """

    pass
