function [m, s] = fitting(xdata, ydata, max)
m = zeros(1, max);
s = zeros(1, max);

% single floating point precision
s_xdata = single(xdata);
s_ydata = single(ydata);

for n=1:max
    % do fit
    p = single(polyfit(s_xdata, s_ydata, n));
    % calc fit values
    f = single(polyval(p, s_xdata));
    % calc fit difference
    df = s_ydata - f;
    m(n) = mean(df);
    s(n) = std(df);
end
end