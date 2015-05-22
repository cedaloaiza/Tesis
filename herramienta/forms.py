from django import forms


opciones_anio = []
for y in range(2002, 2015):
    opciones_anio.append((y,y))

class ClasificadorFormulario(forms.Form):
    #filename = forms.CharField(max_length=100)
    file_entrenamiento = forms.FileField(
        label='Selecciona el archivo de entrenamiento'
    )
    file_prueba = forms.FileField(
        label='Selecciona el archivo de prueba'
    )

class ConstructorTrainTestFormulario(forms.Form):
    file_corpus = forms.FileField(
        label='Selecciona el dataset que quiere dividir'
    )
    eleccion = forms.ChoiceField(choices=opciones_anio)
