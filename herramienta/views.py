from django.shortcuts import render, redirect#, renter_to_response
from herramienta.forms import ClasificadorFormulario,  ConstructorTrainTestFormulario
from herramienta.clasificador import NaiveBayes
from herramienta.preprocesamiento.corpus import construir_entrenamiento_prueba, Corpus

DIRECTORIO_ARCHIVOS = 'herramienta/preprocesamiento/archivosPruebas/'
 
def upload_file(request):
    if request.method == 'POST':
        form = ClasificadorFormulario(request.POST, request.FILES)
        if form.is_valid():
            entrenamiento = request.FILES['file_entrenamiento']
            prueba = request.FILES['file_prueba']
            test = open(DIRECTORIO_ARCHIVOS+prueba.name, 'w')
            test.write(prueba.read())
            training = open(DIRECTORIO_ARCHIVOS+entrenamiento.name, 'w')
            training.write(entrenamiento.read())
            test.close()
            training.close()


            #print('Primera linea', training.readline())
            #print('Segunda linea', training.readline())
            nb = NaiveBayes(open(DIRECTORIO_ARCHIVOS+entrenamiento.name), archivo_prueba=open(DIRECTORIO_ARCHIVOS+prueba.name))
            nb.medidas()
            entrenamiento.readline()
            entrenamiento.readline()
            #print('hola', entrenamiento.readline())
            #print request.POST
            return redirect("uploads")
    else:
        form = ClasificadorFormulario()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'upload.html', {'form': form})

def construir_entrenamiento_prueba_vista(request):
    if request.method == 'POST':
        form = ConstructorTrainTestFormulario(request.POST, request.FILES)
        if form.is_valid():
            corpus = request.FILES['file_corpus']
            opcion = request.POST['eleccion']
            filename = DIRECTORIO_ARCHIVOS+corpus.name
            corpus_archivo = open(filename, 'w')
            corpus_archivo.write(corpus.read())
            corpus_archivo.close()
            construir_entrenamiento_prueba(filename, int(opcion), Corpus.DIRECTORIO_CVS)
            return redirect("divisor")
    else:
        form = ConstructorTrainTestFormulario()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'upload.html', {'form': form})

# Create your views here.
