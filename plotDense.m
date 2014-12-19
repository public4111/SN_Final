X = load('densi_data.txt');
loglog(X(:,1),X(:,2));
xlabel('Number of nodes');
ylabel('Sum of weights');