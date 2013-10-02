# -*- coding: utf-8 -*-
from django.utils import formats, six
from django.forms.util import flatatt
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from datetime import timedelta
from django.conf import settings

DAYS_PER_WEEK = getattr(settings, "DAYS_PER_WEEK", 7)
HOURS_PER_DAY = getattr(settings, "HOURS_PER_DAY", 24)

class DurationInput(TextInput):
    def render(self, name, value, attrs=None):
        """
        output.append(u'<li>%(cb)s<label%(for)s>%(label)s</label></li>' % {"for": label_for, "label": option_label, "cb": rendered_cb})
        """
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            if isinstance(value, six.integer_types):
                value = timedelta(microseconds=value)

            # Otherwise, we've got a timedelta already

            final_attrs['value'] = force_text(DurationInput.format_output(value))
        return mark_safe('<input%s />' % flatatt(final_attrs))
    
    @staticmethod
    def format_output(value):
        '''
        Renders the given timedelta as string of format "3w 2d 5h 30m."
        '''
        weeks, remainder = divmod(value.total_seconds(), 3600 * HOURS_PER_DAY * DAYS_PER_WEEK)
        days, remainder = divmod(remainder, 3600 * HOURS_PER_DAY)
        hours, remainder = divmod(remainder, 3600)  
        minutes, seconds = divmod(remainder, 60)        
        if(weeks > 0):     
            return '%dw %dd %dh %dm' % (weeks, days, hours, minutes)
        elif (days > 0):
            return '%dd %dh %dm' % (days, hours, minutes)
        elif (hours > 0):
            return '%dh %dm' % (hours, minutes)
        else:
            return '%dm' % (minutes)
