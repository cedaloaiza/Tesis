#!/usr/bin/env python
# -*- coding: utf-8 -*-

class NaiveBayes:
    #corpus = open('corpus.csv', 'r')
    #Cantidad de documentos relevantes en el conjunto i
    ni1 = []
    #Cantidad de documentos relevantes fuera del conjunto i
    nni1 = []
    #Cantidad de documentos no relevantes en el conjunto i
    ni0 = []
    #Cantidad de documentos no relevantes fuera del conjunto i
    nni0 = []
    #Cantidad de documentos relevantes
    n1 = 0
    #Cantidad de documentos no relevantes
    n0 = 0
    #Cantidad de documentos
    n = 0
    #Clasificación hecha a un test
    clasificadosNB = []
    #
    clasificadosExperto = []

    def __init__(self, archivo_entrenamiento):
        #print (3)
        self.corpus = archivo_entrenamiento
        self.corpus.readline()
        linea = self.corpus.readline()
        x = linea.split(',')
        #print (x[2] == 'False\n')
        self.cantAtributos = len(x) - 1
        self.inicializarVariablesModelo()
    #self.ni1[0] += 3
    #print (self.cantAtributos+2)
    def contar(self):
        for linea in self.corpus:
            #Para quitar el salto de linea \n
            linea = linea[:-1]
            x = linea.split(',')

            for i in range(self.cantAtributos ):
                #print("x2:", x[2])
                if(x[i] == '1'):
                    if (x[self.cantAtributos]  == '1'):
                        self.ni1[i] += 1
                    elif (x[self.cantAtributos]  == '0'):
                        self.ni0[i] += 1
                elif(x[i] == '0'):
                    if (x[self.cantAtributos]  == '1'):
                        self.nni1[i] += 1
                    elif (x[self.cantAtributos]  == '0'):
                        self.nni0[i] += 1

            if (x[self.cantAtributos]  == '1'):
                self.n1 += 1
            elif (x[self.cantAtributos]  == '0'):
                self.n0 += 1
            self.n += 1
        print (self.ni1, self.nni1, self.n, self.n0, self.n1)
        self.corpus.close

    def inicializarVariablesModelo(self):
        self.ni1 = [None]*self.cantAtributos
        self.nni1 = [None]*self.cantAtributos
        self.ni0 = [None]*self.cantAtributos
        self.nni0 = [None]*self.cantAtributos
        self.clasificadosNB = []
        self.clasificadosExperto = []

        for i in range(self.cantAtributos):
            self.ni1[i] = 0
            self.nni1[i] = 0
            self.ni0[i] = 0
            self.nni0[i] = 0
        #print (self.ni1, self.nni1)

    def clasificar(self, documento):
        #documento = archivo_prueba
        documento.readline()
        for i, linea in enumerate(documento):
            probabilidad1 = self.obtenerProbabilidadRelevante(linea)
            probabilidad0 = self.obtenerProbabilidadNoRelevante(linea)
            print "Probabilidad de que el documento "+str(i+1)+" sea relevante: ", (probabilidad1/float((probabilidad1 + probabilidad0)))*100,"%"
            print "Probabilidad de que el documento "+str(i+1)+" no sea relevante: ", (probabilidad0/float((probabilidad1 + probabilidad0)))*100,"%"
            if( max(probabilidad1, probabilidad0) == probabilidad1 ):
                print "El documento "+str(i+1)+" ha sido clasificado como Relevante"
                self.clasificadosNB.append('1')
            else:
                print "El documento "+str(i+1)+" ha sido clasificado como No Relevante"
                self.clasificadosNB.append('0')

    def obtenerProbabilidadRelevante(self, linea):
        linea = linea[:-1]
        probabilidad = [None]*self.cantAtributos
        x = linea.split(',')
        for i in range(self.cantAtributos ):
            if(x[i] == '1'):
                probabilidad[i] = (self.ni1[i] + 1) / float((self.n1 + self.cantAtributos))
            elif(x[i] == '0'):
                probabilidad[i] = (self.nni1[i] + 1) / float((self.n1 + self.cantAtributos))
        apriori = self.n1 / float(self.n)
        print "probabilidades relevante: ",probabilidad, "Apriori: ", apriori
        self.clasificadosExperto.append(x[self.cantAtributos])
        posteori = self.productoria(probabilidad) * apriori
        return posteori

    def obtenerProbabilidadNoRelevante(self, linea):
        #documento.seek(0)
        linea = linea[:-1]
        probabilidad = [None]*self.cantAtributos
        x = linea.split(',')
        for i in range(self.cantAtributos):
            if(x[i] == '1'):
                probabilidad[i] = (self.ni0[i] + 1) / float((self.n0 + self.cantAtributos))
            elif(x[i] == '0'):
                probabilidad[i] = (self.nni0[i] + 1) / float((self.n0 + self.cantAtributos))
        apriori = self.n0 / float(self.n)
        print"probabilidades no relevantes: ",probabilidad, "Apriori: ", apriori

        posteori = self.productoria(probabilidad) * apriori
        return posteori



    def productoria(self, probabilidad):
        productoria = 1
        for i in probabilidad:
            productoria *= i
        return productoria

    def medidas(self):
        #parece que esta línea no hace nada. :p
        #testC = open("testComprobacion.csv")
        recuperadosYRelevantes = 0
        recuperados = 0
        relevantes = 0
        clasificados_bien = 0
        for i in range(len(self.clasificadosNB)):
            if(self.clasificadosNB[i] == '1' and self.clasificadosExperto[i] == '1'):
                recuperadosYRelevantes +=1
                recuperados += 1
                relevantes += 1
            elif (self.clasificadosNB[i] == '1'):
                recuperados += 1
            elif (self.clasificadosExperto[i] == '1'):
                relevantes += 1
            if (self.clasificadosNB[i] == self.clasificadosExperto[i]):
                clasificados_bien += 1
        print 'Presicion: '+str(recuperadosYRelevantes/float(recuperados))
        print 'Recall: '+str(recuperadosYRelevantes/float(relevantes))
        print 'Accuracy: '+str(clasificados_bien/float(len(self.clasificadosNB)))
        print 'Clasificados bien: '+str(clasificados_bien)






# # #print (2)
# nb = NaiveBayes(open('corpusUnivalle.csv'))
# # #nb = NaiveBayes('corpusUnivalleTraining.csv')
# # #nb = NaiveBayes('corpusBusquedaInicial.csv')
# #nb.corpus = open('corpusBusquedaInicial.csv', 'r')
# nb.contar()
# #nb.clasificar('corpusUnivalle.csv')
# # #nb.clasificar('corpusUnivalleTest.csv')
# nb.clasificar(open('corpusUnivalle.csv'))
# #nb.corpus = open('corpusBusquedaInicial.csv', 'r')
# # print(nb.clasificadosNB)
# # print(nb.clasificadosExperto)
# nb.medidas()
# # #print (nb.productoria([1,2,3]))




		
		
	
