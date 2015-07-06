## Decomposing tests between mixture models into their components 
## Multidimensional case

This work is based on the section **5.4 Decomposing tests between mixture models into their components** 
of the paper [Approximating Likelihood Ratios with Calibrated Discriminative Classifiers]
(http://arxiv.org/abs/1506.02169) by Kyle Cranmer.

We will check the composition method in a 2-dim mixture model. The pdfs conforming the mixture model 
are shown next

![decomposed model](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.10/decomposed_model.png)

Those pdfs forms two mixture models, as shown in formula (21) of the paper of reference.
The first distribution correspond to the null signal hypothesis, meanwhile the second one 
correspond to the mixture model including the signal (in this case the signal corresponds to f0). 
Both distributions for coefficients **c0 = [ 0.,0.3,0.7]** and **c1 = [0.09090909,0.27272727,0.63636364]**
are shown in the next image.

![decomposed model](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.10/full_model.png)

First, the ROC curves obtained by varying the threshold on the trained and true ratios on each pair of 
functions are shown in the next image.

![Decomposed ROC](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.05/dec_comparison_mlp_roc.png)

Next, the Signal Efficiency - Background Rejection curves of each one of the ratios (composed, full trained and full truth) is shown.

![All ROC](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.10/full_comparison_mlp_sigbkg.png)

# Varying the signal presence 

We want to check how the composed and the full strategy are affected when the value of the 
signal coefficient become smaller.

In the next image the mixture models for coefficients for signal of **[0.1,0.05,0.01,0.005]** are 
shown

 0.10                   | 0.05
:-------------------------:|:-------------------------:
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.10/full_model.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.05/full_model.png" width="350" >
 0.01                   | 0.005
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.01/full_model.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.005/full_model.png" width="350" >

Next, the score histogram for each one of the pair-wise trained classifiers for signal 
and background is shown, notice that only histograms for k < j is shown

 0.10                   | 0.05
:-------------------------:|:-------------------------:
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.10/decomp_all_mlp_hist.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.05/decomp_all_mlp_hist.png" width="350" >
 0.01                   | 0.005
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.01/decomp_all_mlp_hist.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.005/decomp_all_mlp_hist.png" width="350" >

The ratio histograms for the composite, full trained and true cases is shown in the next image, those histograms are constructed over data sampled from the distribution of F0 background and f0 signal.

 0.10                   | 0.05
:-------------------------:|:-------------------------:
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.10/ratio_comparison_mlp_hist.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.05/ratio_comparison_mlp_hist.png" width="350" >
 0.01                   | 0.005
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.01/ratio_comparison_mlp_hist.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.005/ratio_comparison_mlp_hist.png" width="350" >


Finally, in the next image the Signal Efficiency - Background Rejection curves for the composed, full trained and true ratio are shown for each one of the cases

 0.10                   | 0.05
:-------------------------:|:-------------------------:
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.10/full_comparison_mlp_sigbkg.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.05/full_comparison_mlp_sigbkg.png" width="350" >
 0.01                   | 0.005
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.01/full_comparison_mlp_sigbkg.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/0.005/full_comparison_mlp_sigbkg.png" width="350" >

It can be seen that for this 2-dim case and very low signal presence the composed ratios are still working perfectly, on the other hand the full trained MLP is not able to 
reproduce the ratio at all.

#N-dimensions

Now, we will check the composition method in a N-dim mixture model. The pdfs conforming the mixture model 
are shown next

![decomposed model](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.10/decomposed_model.png)

Those pdfs forms two mixture models, as shown in formula (21) of the paper of reference.
The first distribution correspond to the null signal hypothesis, meanwhile the second one 
correspond to the mixture model including the signal (in this case the signal corresponds to f0). 
Both distributions for coefficients **c0 = [ 0.,0.3,0.7]** and **c1 = [0.09090909,0.27272727,0.63636364]**
are shown in the next image.

![decomposed model](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.10/full_model.png)

The following images show scatter plots between a subset of features for the pairwise combinations 1-2, 1-3 and 2-3
the number of the feature is indicated in the columns and rows of the grid of plots.

# f1-f2
![scatter grid 1](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/dec_truth_0_1_grid.png)

#f1-f3
![scatter grid 2](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/dec_truth_0_2_grid.png)

#f2-f3
![scatter grid 3](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/dec_truth_1_2_grid.png)

Next, a parallel coordinates plot of the distributions F0 background - f0 signal is shown

![parallel](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/paralell_coordinates_F0-f0.png)

First, the ROC curves obtained by varying the threshold on the trained and true ratios on each pair of 
functions are shown in the next image.

![Decomposed ROC](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.05/dec_comparison_mlp_roc.png)

Next, the Signal Efficiency - Background Rejection curves of each one of the ratios (composed, full trained and full truth) is shown.

![All ROC](https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.10/full_comparison_mlp_sigbkg.png)

# Varying the signal presence 

We want to check how the composed and the full strategy are affected when the value of the 
signal coefficient become smaller.

In the next image the mixture models for coefficients for signal of **[0.1,0.05,0.01,0.005]** are 
shown

 0.10                   | 0.05
:-------------------------:|:-------------------------:
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.10/full_model.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.05/full_model.png" width="350" >
 0.01                   | 0.005
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.01/full_model.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.005/full_model.png" width="350" >

Next, the score histogram for each one of the pair-wise trained classifiers for signal 
and background is shown, notice that only histograms for k < j is shown

 0.10                   | 0.05
:-------------------------:|:-------------------------:
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.10/decomp_all_mlp_hist.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.05/decomp_all_mlp_hist.png" width="350" >
 0.01                   | 0.005
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.01/decomp_all_mlp_hist.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.005/decomp_all_mlp_hist.png" width="350" >

The ratio histograms for the composite, full trained and true cases is shown in the next image, those histograms are constructed over data sampled from the distribution of F0 background and f0 signal.

 0.10                   | 0.05
:-------------------------:|:-------------------------:
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.10/ratio_comparison_mlp_hist.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.05/ratio_comparison_mlp_hist.png" width="350" >
 0.01                   | 0.005
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.01/ratio_comparison_mlp_hist.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.005/ratio_comparison_mlp_hist.png" width="350" >


Finally, in the next image the Signal Efficiency - Background Rejection curves for the composed, full trained and true ratio are shown for each one of the cases

 0.10                   | 0.05
:-------------------------:|:-------------------------:
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.10/full_comparison_mlp_sigbkg.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.05/full_comparison_mlp_sigbkg.png" width="350" >
 0.01                   | 0.005
<img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.01/full_comparison_mlp_sigbkg.png" width="350">  | <img src="https://github.com/jgpavez/systematics/blob/multidim/plots/mlp/10dim/0.005/full_comparison_mlp_sigbkg.png" width="350" >

For this N dimensional case all ratios behave better, still is clear than for smaller signal coefficient the trained ratios are working almost perfectly for the composed 
case.

