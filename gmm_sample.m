%data = csvread('min_normalize.csv');
data = csvread('pca_minimized_17.csv');
%X = data(1:30000,:);
X = data;
obj = fitgmdist(X,10);
idx = cluster(obj,X,'Regularize',10);


