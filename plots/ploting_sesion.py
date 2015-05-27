# coding: utf-8
import numpy as np
c_ratio_log = np.loadtxt('logistic/ratio_classifier.txt')
c_ratio_log = np.loadtxt('logistic/ratio_classifier.txt')
c_ratio_log = np.loadtxt('logistic/ratio_classifier_full.txt')
c_ratio_svr = np.loadtxt('svr/ratio_classifier_full.txt')
c_ratio_svc = np.loadtxt('svc/ratio_classifier_full.txt')
log = plt.plot(x, c_ratio_log, label='Logistic')
x = np.linspace(0,5,100)
import matplotlib.pyplot as plt
log = plt.plot(x, c_ratio_log, label='Logistic')
svr = plt.plot(x, c_ratio_svr, label='SVR')
svc = plt.plot(x, c_ratio_svc, label='SVC')
ratio = np.loadtxt('logistic/ratio.txt')
ratio = np.loadtxt('logistic/ratios_full.txt')
rat = plt.plot(x, ratio, label='Ratio')
plt.xlabel('x')
plt.ylabel('ratios')
plt.legend()
plt.savefig('all_ratios.png')
c_diff_log = np.loadtxt('logistic/ratios_diff_full.txt')
c_diff_svr = np.loadtxt('svr/ratios_diff_full.txt')
c_diff_svc = np.loadtxt('svc/ratios_diff_full.txt')
plt.clf()
log_dif = plt.plot(x, c_diff_log, label='Logistic')
svr_dif = plt.plot(x, c_diff_svr, label='SVR')
svc_dif = plt.plot(x, c_diff_svc, label='SVC')
plt.xlabel('x')
plt.ylabel('difference')
plt.legend()
plt.savefig('all_ratios_diff.png')
plt.clf()
 c_full_log = np.loadtxt('logistic/pdf_ratio_F0_F1_full.txt')
c_full_log = np.loadtxt('logistic/pdf_ratio_F0_F1_full.txt')
log = plt.plot(x, c_ratio_log, label='Decomposed')
full = plt.plot(x, c_full_log, label='Full')
plt.xlabel('x')
plt.ylabel('ratio')
rat = plt.plot(x, ratio, label='Ratio')
plt.title('Ratios for Logistic')
plt.legend()
plt.savefig('ratios_logistic.png')
plt.clf()
c_full_diff = np.loadtxt('logistic/full_ratio_diff.txt')
c_full_diff = np.loadtxt('logistic/full_ratio_diff_full.txt')
plt.plot(x, c_full_diff, label="Full")
plt.plot(x, x_diff_log, label="Decomposed")
plt.plot(x, c_diff_log, label="Decomposed")
plt.xlabel('x')
plt.ylabel('difference')
plt.legend()
plt.title('Differences for Logistic')
plt.savefig('logistic_diff.png')
fig = plt.figure()
ax1 = fig.add_subplot(211)
log = ax1.plot(x, c_ratio_log, label='Decomposed')
full = ax1.plot(x, c_full_log, label='Full')
ax1.xlabel('x')
plt.clf()
roc_f0_f1 = np.loadtxt('logistic/roc_f0_f1.txt')
roc_f0_f2 = np.loadtxt('logistic/roc_f0_f2.txt')
roc_f1_f2 = np.loadtxt('logistic/roc_f1_f2.txt')
roc_F0_F1 = np.loadtxt('logistic/roc_F0_F1.txt')
roc_f0_f1
from sklearn.metrics import roc_curve, auc
roc_f0_f1_auc = auc(roc_f0_f1[0],roc_f0_f1[1])
roc_f0_f1[0]
roc_f0_f1[:,0]
roc_f0_f1[:,1]
roc_f0_f1_auc = auc(roc_f0_f1[:,0],roc_f0_f1[:,1])
roc_f0_f2_auc = auc(roc_f0_f2[:,0],roc_f0_f2[:,1])
roc_f1_f2_auc = auc(roc_f1_f2[:,0],roc_f1_f2[:,1])
roc_F0_F1_auc = auc(roc_F0_F1[:,0],roc_F0_F1[:,1])
plt.figure()
plt.plot(roc_f0_f1[:,0], roc_f0_f1[:,1], label='ROC curve (area = %0.2f)' % roc_f0_f1_auc)
plt.plot(roc_f0_f2[:,0], roc_f0_f2[:,1], label='ROC curve (area = %0.2f)' % roc_f0_f2_auc)
plt.plot(roc_f1_f2[:,0], roc_f1_f2[:,1], label='ROC curve (area = %0.2f)' % roc_f1_f2_auc)
plf.clf()
plt.clf()
plt.figure()
plt.plot(roc_f0_f1[:,0], roc_f0_f1[:,1], label='ROC f0-f1 (area = %0.2f)' % roc_f0_f1_auc)
plt.plot(roc_f0_f2[:,0], roc_f0_f2[:,1], label='ROC f0-f2 (area = %0.2f)' % roc_f0_f2_auc)
plt.plot(roc_f1_f2[:,0], roc_f1_f2[:,1], label='ROC f1-f2 (area = %0.2f)' % roc_f1_f2_auc)
plt.plot(roc_F0_F1[:,0], roc_F0_F1[:,1], label='ROC F0-F1 (area = %0.2f)' % roc_F0_F1_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curves for logistic')
plt.legend(loc="lower right")
plt.savefig('roc_curves.png')
get_ipython().magic(u'save ploting_sesion')
get_ipython().magic(u'save ploting_sesion.py')
get_ipython().magic(u'save ploting_sesion.py 1-94')