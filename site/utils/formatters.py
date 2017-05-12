#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import re

logger = logging.getLogger(__name__)


def human_readable_segments(segments):
    return u', '.join([str(s) for s in segments])


def flatten_list(nested_list):
    """
    flattens a list from [[a,b]. [c,d]] to [a,b,c,d]
    from http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    """
    return [item for sublist in nested_list for item in sublist]


def string_list_to_json(string):
    """
    takes string and converts into list: "1,2,3,4-10"
    to [1,2,3,u'4-10']
    """
    # validate first
    pattern = re.compile(r'[^0-9,\- ]')
    if pattern.findall(string):
        raise ValueError('invalid characters in segments list')

    parts = string.split(",")
    res = []
    for part in parts:
        if part == '':
            continue
        part = part.strip()
        if part.count('-') == 1:
            res.append(unicode(part))
        elif part.count('-') == 0 and len(part) > 0:
            res.append(int(part))
        else:
            logger.warning('attempt to add badly formatted number segment',
                           extra={'string': part})

    res = deflate_segments(inflate_segments(res))

    return res


def inflate_segments(segments):
    """
    change all shortened segments u'1-10' into [1,2 ..., 10]
    also standardizes format:
    * ordered
    * deflated
    * no duplicates
    """
    def to_list(segment):
        if isinstance(segment, unicode) and '-' in segment:
            start, end = segment.split('-')
            return range(int(start), int(end)+1)

        return segment

    nested_segments = [to_list(segment)for segment in segments]
    flattened_segments = []
    for segment in nested_segments:
        if isinstance(to_list(segment), int):
            flattened_segments.append(segment)
        if isinstance(to_list(segment), list):
            flattened_segments.extend(segment)

    flattened_segments.sort()
    return flattened_segments


def deflate_segments(segments):
    """
    inverted inflate_segments method by:
    * using range where possible
    * remove duplicates
    * sort
    """

    if len(segments) == 0:
        return []

    # --- standardize on deflate
    # remove dupes
    segments = list(set(segments))
    # sort
    segments.sort()  # mandatory, but perf wasting

    start = None
    advance = None
    deflated_segments = []
    last_segment = segments[-1]

    # attention: writes to list backwards elements
    for segment in segments:
        if start is None:
            start = segment
            advance = segment
            # if this is a one element list
            if segment == last_segment:
                deflated_segments.append(start)
            continue
        elif advance and segment == advance + 1:
            advance = segment
            # on last element write range before continue
            if segment == last_segment:
                deflated_segments.append(u'{}-{}'.format(start, advance))
            continue

        # write single int
        if start == advance:
            deflated_segments.append(start)
        else:
            deflated_segments.append(u'{}-{}'.format(start, advance))

        # on last element detect and write lonely int
        if segment == last_segment and segment > advance + 1:
            deflated_segments.append(segment)

        # start over
        start = segment
        advance = segment

    return deflated_segments


def make_numeric(text):
    import re
    return re.sub("[^0-9]", "", text)
