#!/usr/bin/env python
# -*- coding: utf-8 -*-
from manejadorArchivos import leer_archivo, obtener_autores
from corpus import Corpus
from herramienta.clasificador import NaiveBayes



class Experimento:
    '''Esta clase representa un conjunto de experimentos para un caso en especifico. contruye corpus y genera resultados'''
    def __init__(self, directorio, escuela, tamanio, tipo_experimento, anios):
        '''Parametros:
        Directorio(string):Directorio del experimento
        Escuela(String):Escuela del experimento
        tamanio(String): Indica si el corpus va a ser toda la U o la BI
        tipo_experimento(String): Indica con cuáles medidas se va a construir el dataset
        anios(Range): Rango de los años con los que se va a predecir'''
        self.directorio = directorio
        self.anio = anios
        self.tamanio = tamanio
        self.nombre_corpus = '%sCorpusExperimentos/%s%s%sCorpus.csv'%(directorio, escuela, tamanio, tipo_experimento)
        print self.nombre_corpus
        self.contruir_corpus_experimento()

    def contruir_corpus_experimento(self):
        '''Contruye el dataset'''
        c = Corpus()
        if self.tamanio == 'BI':
            busquedaInicial=leer_archivo(open(self.directorio+'bi.csv','r'), eliminar_primero=True)
            clasificados = leer_archivo(open(self.directorio+'clasificados.csv', 'r'),eliminar_primero=True)
        elif self.tamanio == 'Univ':
            busquedaInicial=leer_archivo(open(self.directorio++'dataPapers.csv','r'), eliminar_primero=True)
            clasificados = leer_archivo(open(self.directorio++'validacion.csv', 'r'),eliminar_primero=True)
        conjuntoA=leer_archivo(open(self.directorio+'a.csv','r'),eliminar_primero=True)
        conjuntoS=leer_archivo(open(self.directorio+'s.csv','r'),eliminar_primero=True)
        conjuntoJ=leer_archivo(open(self.directorio+'j.csv','r'),eliminar_primero=True)
        conjuntoO=leer_archivo(open(self.directorio+'o.csv','r'),eliminar_primero=True)

        xmls = self.obtener_xmls()

        #Archivos con los eid de los papers que van a conformar la red
        ##archivo_papers_red = dividir_archivo_fecha(open(self.directorio+'relevantes.csv'), open(self.directorio+'relevantesFecha.csv'), 2013)
        archivo_papers_red = open(self.directorio+'bi.csv')
        #Lista con los eid de los papers que van a conformar la red
        lista_papers_red = leer_archivo(archivo_papers_red, eliminar_primero=True)
        #Autores-papers de la red
        dicci_contruir_red = obtener_autores(xmls, lista_papers_red)
        #Aqué deberían estar todos los autores-papers del corpus
        dicci_todos_autores_papers = obtener_autores(xmls, leer_archivo(open(self.directorio+'bi.csv'), eliminar_primero=True))
        #c.construir_corpus(self.nombre_corpus, busquedaInicial, conjuntoA, conjuntoS, conjuntoJ, conjuntoO, clasificados,
        #                   conjuntos_red=dicci_contruir_red, diccionario_todos_autores=dicci_todos_autores_papers)
        c.construir_corpus(self.nombre_corpus, busquedaInicial, conjuntoA, conjuntoS, conjuntoJ, conjuntoO, clasificados)
    def obtener_xmls(self):
        return [open('XMLs/xml0.xml'),open('XMLs/xml1.xml'),open('XMLs/xml2.xml'),open('XMLs/xml3.xml')]

    def correr_exp_prueba_experimento(self, fechaDivision):
        '''Corre el experimento de predicción con el test empezando desde la fechaDivision'''
        print type(fechaDivision)
        fechas = open(self.directorio+'fechas.csv')
        #fechas = open('herramienta/preprocesamiento/'+directorio+'fechasUniversidad.csv')
        corpus = open(self.nombre_corpus)
        nombreCorpus=self.nombre_corpus.replace('.csv', '')
        nombre_entrenamiento = nombreCorpus+'Entrenamiento'+str(fechaDivision-1)+'.csv'
        nombre_prueba = nombreCorpus+'Prueba'+str(fechaDivision)+'.csv'
        entrenamiento = open(nombre_entrenamiento, 'w')
        prueba = open(nombre_prueba, 'w')
        fechas.readline()
        encabezado = corpus.readline()
        entrenamiento.write(encabezado)
        prueba.write(encabezado)
        encabezado2 = corpus.readline()
        entrenamiento.write(encabezado2)
        prueba.write(encabezado2)

        for fecha, instancia in zip(fechas, corpus):
            #print int(fecha.rstrip())>=fechaDivision
            if(int(fecha.rstrip())>=fechaDivision):
                prueba.write(instancia)
            else:
                entrenamiento.write(instancia)
        entrenamiento.close()
        prueba.close()
        entrenamiento = open(nombre_entrenamiento, 'r')
        prueba = open(nombre_prueba, 'r')

        nb = NaiveBayes(entrenamiento, prueba)
        nb.medidas()

def prueba():

    directorios = [Corpus.DIRECTORIO_CVS, Corpus.DIRECTORIO_INDUSTRIAL, Corpus.DIRECTORIO_INGENIERIA, Corpus.DIRECTORIO_PITTS]
    escuelas =['eisc', 'industrial', 'ingenieria', 'pitts']
    anios = ['2010', '2009', '2008']
    experimentos = []
    e = Experimento(Corpus.DIRECTORIO_CVS, 'eisc', 'BI', 'Base', range(5))
    e.correr_exp_prueba_experimento(2013)

prueba()