K = 10;
d = 17;
N = 438928;
data = csvread('pca_minimized_17.csv');
size(data)
X = data(1:N,:);
mu = randn(K,d);
for k = 1:K
    Sigma(:,:,k) = eye(d);
end
%Sigma = randn(d,d,K);
pi = 1/K * ones(1,K);

gamma = zeros(N,K);
iter = 0;
lamda = 1;
nnz(isnan(gamma))
while true

    % E step
    for i=1:N
        x_i = X(i,:);
        row_sum = 0;
        for k = 1 : K
            tmp_density = mvnpdf(x_i, mu(k,:), Sigma(:,:,k));
            row_sum = row_sum + tmp_density;
            gamma(i, k) = tmp_density;
        end
        gamma(i, :) = (1 / row_sum) * gamma(i, :);
        if nnz(isnan(gamma(i, :))) > 0
            gamma(i, :) = (1 / k) * ones(1, k);
        end
        assert(nnz(isnan(gamma(i, :))) == 0);
    end

    %M step
     N_k = sum(gamma);
     for k=1:K
         mu_tmp = zeros(1, d);
         sigma_tmp = zeros(d, d);
         
         % get new mu_k
         for n=1:N
             mu_tmp = mu_tmp + gamma(n,k) * X(n, :);
         end
         mu_tmp = 1 / N_k(k) * mu_tmp;
         mu(k, :) = mu_tmp;
         
         % get new sigma_k
         for n=1:N
             x_n = X(n, :);
             x_n_diff = x_n - mu_tmp;
             sigma_tmp = sigma_tmp + gamma(n,k) * (x_n_diff' * x_n_diff);
         end
         sigma_tmp = 1 / N_k(k) * sigma_tmp;
         Sigma(:,:,k) = sigma_tmp;
         
         pi(k) = 1 / N_k(k) / N;
     end

    iter = iter + 1
end
