from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .util import wordnet_similarity

class KanjiTestForm(forms.Form):
    answer = forms.CharField()
    current_index = forms.IntegerField(widget=forms.HiddenInput(), initial=0)  # Add this hidden field for current index

    helper = FormHelper()
    helper.form_method = 'post'
    helper.layout = Layout(
        Field('answer', css_class='user-answer', id='user-answer-field'),
        Submit('submit', 'Submit'),
    )

    def is_answer_correct(self, correct_answer):
        user_answer = self.cleaned_data.get('answer')
        similarity = wordnet_similarity(user_answer, correct_answer)
        return similarity >= 0.7
