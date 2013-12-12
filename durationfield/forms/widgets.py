# -*- coding: utf-8 -*-
from django.utils import six
from django.forms.util import flatatt
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from datetime import timedelta
from django.conf import settings
from durationfield.utils.timestring import timedelta_to_string

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
            
            if isinstance(value, unicode):
                final_attrs['value'] = force_text(value)
            else:
                # Only add the 'value' attribute if a value is non-empty.
                if isinstance(value, six.integer_types):
                    value = timedelta(microseconds=value)
    
                # Otherwise, we've got a timedelta already
                if final_attrs.has_key('hour_is_max_unit') and final_attrs['hour_is_max_unit']: 
                    final_attrs['value'] = force_text(timedelta_to_string(value, True))
                else:  
                    final_attrs['value'] = force_text(timedelta_to_string(value))
                
        return mark_safe('<input%s />' % flatatt(final_attrs))


class DurationByHourInput(DurationInput):
    def render(self, name, value, attrs=None):
        attrs['hour_is_max_unit'] = True
        return super(DurationByHourInput, self).render(name, value, attrs)

