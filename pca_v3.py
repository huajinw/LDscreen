from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

n = 40	# number of components

data = np.loadtxt('outnormalize.csv',delimiter=',')
data = np.nan_to_num(data)
pca = PCA(n_components = n)
result = pca.fit(data).transform(data)
np.savetxt('pca_result_%d.csv' % n,result,delimiter=',')

#The amount of variance that each PC explains
loadings= pca.explained_variance_ratio_

#Cumulative Variance explains
loadings_cum=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)

print(loadings)
np.savetxt('loadings.csv',loadings, delimiter = ',')
np.savetxt('loadings_cum.csv',loadings_cum, delimiter = ',')


fig1 = plt.plot(loadings)
plt.savefig('loadings')
fig2 = plt.plot(loadings_cum)
plt.savefig('loadings_cum')
