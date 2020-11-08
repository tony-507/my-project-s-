function [] = plotMdlData(data)
% Reproduce the plots from ex2 with positive and negative results for an input table
% Extract variable names from 3 column table
varNames = data.Properties.VariableNames;
% Plot the data with + for true and 0 for false examples
inds = data.(varNames{3}) == 1;
plot(data.(varNames{1})(inds), data.(varNames{2})(inds), 'k+','LineWidth', 2, 'MarkerSize', 7); 
inds = data.(varNames{3}) == 0;
plot(data.(varNames{1})(inds), data.(varNames{2})(inds), 'ko', 'MarkerFaceColor', 'y','MarkerSize', 7);
end
