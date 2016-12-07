K = 10;
d = 17;
N = 438928;
% N = 3000;
data = csvread('pca_minimized_17.csv');
size(data)
X = data(1:N,:);
Mu = dlmread('./k10/Mu_kmeans.txt');
for k = 1:K
    Sigma(:,:,k) = eye(d);
end
%Sigma = randn(d,d,K);
Pi = 1/K * ones(1,K);

gamma = zeros(N,K);
iter = 0;
lamda = 1;
nnz(isnan(gamma))
while true

    % E step
    parfor (i=1:N, 16)
        x_i = X(i,:);
        row_sum = 0;

        tmp_vector = zeros(1,K);
        for k = 1 : K
            tmp_density = mvnpdf(x_i, Mu(k,:), Sigma(:,:,k));
            row_sum = row_sum + tmp_density;
            tmp_vector(k) = tmp_density;
        end
        gamma(i, :) = (1 / row_sum) * tmp_vector;
        if nnz(isnan(gamma(i, :))) > 0
            gamma(i, :) = (1 / k) * ones(1, k);
        end
        assert(nnz(isnan(gamma(i, :))) == 0);
    end

    %M step
     N_k = sum(gamma);
     parfor (k=1:K, 8)
         % get new mu_k
         mu_tmp = (gamma(:,k))' * X;
         mu_tmp = 1 / N_k(k) * mu_tmp;
         Mu(k, :) = mu_tmp;
         sigma_tmp = zeros(d, d);
         
         % get new sigma_k
         for n=1:N
             x_n = X(n, :);
             x_n_diff = x_n - mu_tmp;
             sigma_tmp = sigma_tmp + gamma(n,k) * (x_n_diff' * x_n_diff);
         end
         sigma_tmp = 1 / N_k(k) * sigma_tmp;
         Sigma(:,:,k) = sigma_tmp;
         
         Pi(k) = 1 / N_k(k) / N;
     end

    iter = iter + 1
    
    if mod(iter, 20) == 0
        dlmwrite(sprintf('Pi_%d.txt', iter), Pi);
        dlmwrite(sprintf('Sigma_%d.txt', iter),Sigma);
        dlmwrite(sprintf('Mu_%d.txt', iter), Mu);
    end
end
