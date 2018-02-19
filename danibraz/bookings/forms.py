from django import forms
from danibraz.users.models import User

from django.contrib.admin.widgets import FilteredSelectMultiple

from material import Fieldset
from material import Layout
from material import Row
from material import Span6


from danibraz.bookings.models import Booking


class BookingsForm(forms.ModelForm):
    allday = forms.BooleanField(label='Dia inteiro', required=False)
    title = forms.CharField(label='Titulo do agendamento')
    start = forms.DateTimeField(label='Inicia em...')
    end = forms.DateTimeField(label='Termina em...')
    #created_on = forms.DateTimeField(label='Criado em...')
    authorized = forms.BooleanField(label='Autorizado', required=False)
    editable = forms.BooleanField(label='Editavel', required=False)
    # ABAIXO, CHOICES NO FORMS VAI TER UMALISTAGEM NO TEMPLATE
    color = forms.ChoiceField(label='Cor', choices=(('blue', 'blue'),
                                                    ('red', 'red'),
                                                    ('green', 'green'),
                                                    ('black', 'black')))
    overlap = forms.BooleanField(label='Sobrepor?', required=False)
    holiday = forms.BooleanField(label='Feriado?', required=False)
    participants = forms.ModelMultipleChoiceField(label='Participantes', queryset=User.objects.all(), widget=FilteredSelectMultiple("Participantes", is_stacked=False, attrs={'class':'material-ignore', 'multiple':'True'}))

    class Meta:
        model = Booking
        exclude = ['created_on']
        fields = '__all__'

    layout = Layout(
        Fieldset('Inclua uma agenda',
                 Row('title', ),
                 Row('start','end', 'color'),
                 Row(Span6('holiday'),Span6('authorized'), ),
                 Row(Span6('editable'), Span6('allday')),
                 Row('overlap'),
                 Row('participants')
                 )
    )