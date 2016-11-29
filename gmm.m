K = 10;
d = 17;
%N = 3000;
N = 30000;
data = csvread('pca_minimized_17.csv');
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

while true
    % E step
    for i=1:N
        gamma(i,:) =(pi .* mvnpdf(X(i,:), mu, Sigma)') / (pi * mvnpdf(X(i,:), mu, Sigma));
    end
    gamma(isnan(gamma)) = 0;
    %M step
    N_k = sum(gamma);
    denominator_Nk = repmat((1./N_k),d,1);
    mu = (gamma' * X) .* (denominator_Nk)';
    for k=1:K
        summer = zeros(d);
        for n=1:N
            summer = summer + (X(n,:)-mu(k,:))*(X(n,:)-mu(k,:))';
        end
        Sigma(:,:,k) =  1/N_k(k) * summer + lamda * eye(d);
    end
    pi = N_k / (sum(N_k));
    
    iter = iter + 1
end







