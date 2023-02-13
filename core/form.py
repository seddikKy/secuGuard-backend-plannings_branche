

from django import forms

from core.models import Planning


class PlanningForm(forms.ModelForm):
    from_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    def __init__(self, *args, **kwargs):
       super(PlanningForm, self).__init__(*args, **kwargs)
       self.fields['zone'].required = False
       self.fields['zone'].widget.attrs['disabled'] = "disabled" 
       self.fields['selected_day_index'].required = False
       self.fields['selected_day_index'].widget.attrs['disabled'] = "disabled" 


    class Meta:
        model = Planning
        fields = '__all__'  
       
