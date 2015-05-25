#!/usr/bin/env python
__author__ = "Pavez J. <juan.pavezs@alumnos.usm.cl>"


import ROOT
import numpy as np
from sklearn import svm, linear_model
from sklearn.externals import joblib
from sklearn.metrics import roc_curve, auc

import sys

import os.path
import pdb

import matplotlib.pyplot as plt


''' 
 A simple example for the work on the section 
 5.4 of the paper 'Approximating generalized 
 likelihood ratio test with calibrated discriminative
 classifiers' by Kyle Cranmer
''' 

# Constants for each different model
c0 = [.0,.3, .7]
c1 = [.1,.5, .4]
verbose_printing = True

def printFrame(w,obs,pdf):
  '''
    This just print a bunch of pdfs 
    in a Canvas
  ''' 

  # Hope I don't need more colors ...
  colors = [ROOT.kBlack,ROOT.kRed,ROOT.kGreen,ROOT.kBlue,
    ROOT.kYellow]

  x = w.var(obs)
  funcs = []
  line_colors = []
  for i,p in enumerate(pdf):
    funcs.append(w.pdf(p))
    line_colors.append(ROOT.RooFit.LineColor(colors[i]))
  
  c1 = ROOT.TCanvas('c1')
  frame = x.frame()
  for i,f in enumerate(funcs):
      f.plotOn(frame,line_colors[i])
  frame.Draw()
  c1.SaveAs('plots/model{0}.pdf'.format('-'.join(pdf)))

def makeData(num_train=500,num_test=100):
  '''
  RooFit statistical model for the data
  
  '''  
  # Statistical model
  w = ROOT.RooWorkspace('w')
  w.factory("EXPR::f0('exp(x*-1)',x[0,5])")
  w.factory("EXPR::f1('cos(x)**2 + .01',x)")
  w.factory("EXPR::f2('exp(-(x-2)**2/2)',x)")
  w.factory("SUM::F0(c00[{0}]*f0,c01[{1}]*f1,f2)".format(c0[0],c0[1]))
  w.factory("SUM::F1(c10[{0}]*f0,c11[{1}]*f1,f2)".format(c1[0],c1[1]))
  
  # Check Model
  w.Print()
  w.writeToFile('workspace_DecomposingTestOfMixtureModelsClassifiers.root')
  #printFrame(w,'x',['f0','f1','f2']) 
  #printFrame(w,'x',['F0','F1'])

  # Start generating data
  ''' 
    Each function will be discriminated pair-wise
    so n*n datasets are needed (maybe they can be reused?)
  ''' 
   
  def makeDataset(x,bkgpdf,sigpdf,num):
    traindata = np.zeros(num*2)
    targetdata = np.zeros(num*2)
    bkgdata = bkgpdf.generate(ROOT.RooArgSet(x),num)
    sigdata = sigpdf.generate(ROOT.RooArgSet(x),num)
    
    traindata[:num] = [sigdata.get(i).getRealValue('x') 
        for i in range(num)]
    targetdata[:num].fill(1)

    traindata[num:] = [bkgdata.get(i).getRealValue('x')
        for i in range(num)]
    targetdata[num:].fill(0)
    
    return traindata, targetdata  
 

  x = w.var('x')
  for k,c in enumerate(c0):
    for j,c_ in enumerate(c1):  
      traindata, targetdata = makeDataset(x,w.pdf('f{0}'.format(k)),w.pdf('f{0}'.format(j))
      ,num_train)

      np.savetxt('data/traindata_{0}_{1}.dat'.format(k,j),
              np.column_stack((traindata,targetdata)),fmt='%f')

      testdata, testtarget = makeDataset(x,w.pdf('f{0}'.format(k)),w.pdf('f{0}'.format(j))
      ,num_test)

      np.savetxt('data/testdata_{0}_{1}.dat'.format(k,j),
              np.column_stack((testdata,testtarget)),fmt='%f')


  traindata, targetdata = makeDataset(x,w.pdf('F0'),w.pdf('F1'),num_test)

  np.savetxt('data/traindata_F0_F1.dat',
          np.column_stack((traindata,targetdata)),fmt='%f')

  testdata, testtarget = makeDataset(x,w.pdf('F0'.format(k)),w.pdf('F1'.format(j))
  ,num_test)

  np.savetxt('data/testdata_F0_F1.dat',
          np.column_stack((testdata,testtarget)),fmt='%f')


def loadData(filename):
  traintarget = np.loadtxt(filename)
  traindata = traintarget[:,0]
  targetdata = traintarget[:,1]
  return (traindata, targetdata)

def predict(clf, traindata):
  if clf.__class__.__name__ == 'NuSVR':
    output = clf.predict(traindata)
    return np.clip(output,0.,1.)
  else:
    return clf.predict_proba(traindata)[:,1]

def makeROC(clf, data, label):
  '''
    make plots for ROC curve of classifier and 
    test data.
  '''
  testdata, testtarget = data
  outputs = predict(clf,testdata.reshape(testdata.shape[0],1))
  fpr, tpr, _  = roc_curve(testtarget.ravel(),outputs.ravel())
  roc_auc = auc(fpr, tpr)
  plt.figure()
  plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
  plt.plot([0, 1], [0, 1], 'k--')
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title('ROC {0}'.format(label))
  plt.legend(loc="lower right")
  np.savetxt('plots/roc_{0}.txt'.format(label),np.column_stack((fpr,tpr)))
  plt.savefig('plots/roc_{0}.png'.format(label))
  plt.clf()

def trainClassifier(clf):
  '''
    Train classifiers pair-wise on 
    datasets
  '''

  for k,c in enumerate(c0):
    for j,c_ in enumerate(c1):
      traindata,targetdata = loadData('data/traindata_{0}_{1}.dat'.format(k,j)) 

      print " Training Classifier on f{0}/f{1}".format(k,j)
      #clf = svm.NuSVC(probability=True) #Why use a SVR??
      clf.fit(traindata.reshape(traindata.shape[0],1)
          ,targetdata)
      joblib.dump(clf, 'model/adaptive_{0}_{1}.pkl'.format(k,j))

      testdata, testtarget = loadData('data/testdata_{0}_{1}.dat'.format(k,j)) 
      makeROC(clf, (testdata, testtarget), 'f{0}_f{1}'.format(k,j))
  
  traindata,targetdata = loadData('data/traindata_F0_F1.dat') 
  print " Training Classifier on F0/F1"
  #clf = svm.NuSVC(probability=True) #Why use a SVR??
  clf.fit(traindata.reshape(traindata.shape[0],1)
      ,targetdata)
  joblib.dump(clf, 'model/adaptive_F0_F1.pkl')

  testdata, testtarget = loadData('data/testdata_F0_F1.dat') 
  makeROC(clf, (testdata, testtarget), 'F0_F1')



def classifierPdf():
  ''' 
    Create pdfs for the classifier 
    score to be used later on the ratio 
    test
  '''

  bins = 30
  low = 0.
  high = 1.  

  f = ROOT.TFile('workspace_DecomposingTestOfMixtureModelsClassifiers.root')
  w = f.Get('w')
  f.Close()

  w.factory('score[{0},{1}]'.format(low,high))
  s = w.var('score')

  def saveHistos(w,ouputs,pos=None):
    if pos <> None:
      k,j = pos
    else:
      k,j = ('F0','F1')
    for l,name in enumerate(['sig','bkg']):
      data = ROOT.RooDataSet('{0}data_{1}_{2}'.format(name,k,j),"data",
          ROOT.RooArgSet(s))
      hist = ROOT.TH1F('{0}hist_{1}_{2}'.format(name,k,j),'hist',bins,low,high)
      for val in outputs[l*numtrain/2:(l+1)*numtrain/2]:
        hist.Fill(val)
        s.setVal(val)
        data.add(ROOT.RooArgSet(s))
      
      datahist = ROOT.RooDataHist('{0}datahist_{1}_{2}'.format(name,k,j),'hist',
            ROOT.RooArgList(s),hist)
      s.setBins(bins)
      histpdf = ROOT.RooHistPdf('{0}histpdf_{1}_{2}'.format(name,k,j),'hist',
            ROOT.RooArgSet(s), datahist, 1)
            
      histpdf.specialIntegratorConfig(ROOT.kTRUE).method1D().setLabel('RooBinIntegrator')

      getattr(w,'import')(data)
      getattr(w,'import')(datahist) # work around for morph = w.import(morph)
      getattr(w,'import')(histpdf) # work around for morph = w.import(morph)

      # Calculate the density of the classifier output using kernel density 
      # estimation technique
      w.factory('KeysPdf::{0}dist_{1}_{2}(score,{0}data_{1}_{2})'.format(name,k,j))

      # Print histograms pdfs and estimated densities
      if verbose_printing == True:
        printFrame(w,'score',['{0}histpdf_{1}_{2}'.format(name,k,j)])
        printFrame(w,'score',['{0}dist_{1}_{2}'.format(name,k,j)])

  for k,c in enumerate(c0):
    for j,c_ in enumerate(c1):
      traindata, targetdata = loadData('data/traindata_{0}_{1}.dat'.format(k,j))
      numtrain = traindata.shape[0]       

      clf = joblib.load('model/adaptive_{0}_{1}.pkl'.format(k,j))
      
      # Should I be using test data here?
      outputs = predict(clf,traindata.reshape(traindata.shape[0],1))
      #outputs = clf.predict_proba(traindata.reshape(traindata.shape[0],1)) 
      saveHistos(w,outputs,(k,j))

  traindata, targetdata = loadData('data/traindata_F0_F1.dat')
  numtrain = traindata.shape[0]       

  clf = joblib.load('model/adaptive_F0_F1.pkl')
  
  # Should I be using test data here?
  outputs = predict(clf,traindata.reshape(traindata.shape[0],1))
  #outputs = clf.predict_proba(traindata.reshape(traindata.shape[0],1)) 
  saveHistos(w,outputs)
     
  w.Print()

  w.writeToFile('workspace_DecomposingTestOfMixtureModelsClassifiers.root')

  
# this is not very efficient
def scikitlearnFunc(filename,x=0.):
  '''
    Needed for the scikit-learn wrapper
  '''
  clf = joblib.load(filename)
  traindata = np.array((x))
  outputs = predict(clf,traindata)[0]
  
  #if outputs[0] > 1:
  #  return 1.
  return outputs

class ScikitLearnCallback:
  def __init__(self,file):
    clf = joblib.load(file)

  def get(self,x = 0.):
    train = np.array((x))
    outputs = predict(clf,train)[0]
    
    if outputs[0] > 1:
      return 1.
    return outputs[0]


def fitAdaptive():
  '''
    Use the computed score densities to compute 
    the decompose ratio test
  '''
  ROOT.gSystem.Load('parametrized-learning/SciKitLearnWrapper/libSciKitLearnWrapper')
  ROOT.gROOT.ProcessLine('.L CompositeFunctionPdf.cxx+')


  f = ROOT.TFile('workspace_DecomposingTestOfMixtureModelsClassifiers.root')
  w = f.Get('w')
  f.Close()

  #x = w.var('x[-5,5]')
  x = ROOT.RooRealVar('x','x',0.2,0,5)
  getattr(w,'import')(ROOT.RooArgSet(x),ROOT.RooFit.RecycleConflictNodes()) 

  def constructDensity(w,pos = None):
    if pos <> None:
      k,j = pos
    else:
      k,j = ('F0','F1')
    test = scikitlearnFunc('model/adaptive_{0}_{1}.pkl'.format(k,j),2.0)
    nn = ROOT.SciKitLearnWrapper('nn_{0}_{1}'.format(k,j),'nn_{0}_{1}'.format(k,j),x)
    nn.RegisterCallBack(lambda x: scikitlearnFunc('model/adaptive_{0}_{1}.pkl'.format(k,j),x))
    getattr(w,'import')(ROOT.RooArgSet(nn),ROOT.RooFit.RecycleConflictNodes()) 

    # I should find the way to use this method
    #callbck = ScikitLearnCallback('adaptive_f{0}_f{1}.pkl'.format(k,j))
    #nn.RegisterCallBack(lambda x: callbck.get(x))

    # Inserting the nn output into the pdf graph
    for l,name in enumerate(['sig','bkg']):
      w.factory('CompositeFunctionPdf::{0}template_{1}_{2}({0}dist_{1}_{2})'.
          format(name,k,j))
      w.factory('EDIT::{0}moddist_{1}_{2}({0}template_{1}_{2},score=nn_{1}_{2})'
              .format(name,k,j))
     
    if verbose_printing == True:
      printFrame(w,'x',['sigmoddist_{0}_{1}'.format(k,j),
                'bkgmoddist_{0}_{1}'.format(k,j)])

  for k,c in enumerate(c0):
    for j,c_ in enumerate(c1):
      constructDensity(w,(k,j))
      #w.Print()
      # Save graphs
      #sigpdf.graphVizTree('sigpdfgraph.dot')
      #bkgpdf.graphVizTree('bkgpdfgraph.dot')
      
  constructDensity(w)
  
  # To calculate the ratio between single functions
  def singleRatio(x,f0,f1,val):
    x.setVal(val)
    if f0.getValV() < 10E-10:
      return 0.
    return f1.getValV() / f0.getValV()

  # pair-wise ratios
  # and decomposition computation
  npoints = 100
  xarray = np.linspace(0,5,npoints)
  fullRatios = np.zeros(npoints)
  x = w.var('x')

  def saveFig(x,y,file):
    plt.plot(x,y)
    plt.ylabel('ratio')
    plt.xlabel('x')
    plt.title(file)
    np.savetxt('plots/{0}_full.txt'.format(file),y)
    plt.savefig('plots/{0}.png'.format(file))
    plt.clf()

  for k,c in enumerate(c0):
    innerRatios = np.zeros(npoints)
    if c == 0:
      continue
    for j,c_ in enumerate(c1):
      f0pdf = w.pdf('bkgmoddist_{0}_{1}'.format(k,j))
      f1pdf = w.pdf('sigmoddist_{0}_{1}'.format(k,j))
      f0 = w.pdf('f{0}'.format(k))
      f1 = w.pdf('f{0}'.format(j))
      pdfratios = [singleRatio(x,f0pdf,f1pdf,xs) for xs in xarray]
      # the cases in which both distributions are the same can be problematic
      # one will expect that the classifier gives same prob to both signal and bkg
      # but it can behave in weird ways, I will just avoid this for now 
      pdfratios = np.array(pdfratios) if k <> j else np.ones(npoints)
      innerRatios += (c_/c) * pdfratios
      ratios = [singleRatio(x,f0,f1,xs) for xs in xarray]

      saveFig(xarray, pdfratios,'pdf_ratio_{0}_{1}'.format(k,j))
      saveFig(xarray, ratios, 'ratio_{0}_{1}'.format(k,j))
    fullRatios += 1./innerRatios

  # full ratios
  saveFig(xarray, fullRatios, 'ratio_classifier') 

  y2 = [singleRatio(x,w.pdf('F1'),w.pdf('F0'),xs) for xs in xarray]

  saveFig(xarray, y2, 'ratios')
  saveFig(xarray, np.array(y2) - fullRatios, 'ratios_diff')

  # NN trained on complete model
  F0pdf = w.pdf('bkgmoddist_F0_F1')
  F1pdf = w.pdf('sigmoddist_F0_F1')
  pdfratios = [singleRatio(x,F1pdf,F0pdf,xs) for xs in xarray]
  pdfratios = np.array(pdfratios)
  saveFig(xarray, pdfratios, 'pdf_ratio_F0_F1')
  saveFig(xarray, np.array(y2) - pdfratios, 'full_ratio_diff')

  #w.Print()

if __name__ == '__main__':
  classifiers = {'svc':svm.NuSVC(probability=True),'svr':svm.NuSVR(),
        'logistic': linear_model.LogisticRegression()}
  clf = None
  if (len(sys.argv) > 1):
    clf = classifiers.get(sys.argv[1])
  if clf == None:
    clf = classifiers['logistic']    
    print 'Not found classifier, Using logistic instead'

  # Set this value to False if only final plots are needed
  verbose_printing = True

  makeData(num_train=300) 
  trainClassifier(clf)
  classifierPdf()
  fitAdaptive()

