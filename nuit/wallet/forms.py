from django import forms


LANGUAGES = [('en', 'Ingles'), ('es', 'Espanol')]
NUMBER_OF_WORDS = [('13', '13'), ('15', '15'), ('18', '18'), ('21', '21'), ('24', '24')]

class MnemonicForm(forms.Form):
    language = forms.ChoiceField(widget=forms.Select,
                                         choices=LANGUAGES)
    number_of_words = forms.ChoiceField(widget=forms.Select,
                                               choices=NUMBER_OF_WORDS)
    dice_entropy = forms.CharField()
