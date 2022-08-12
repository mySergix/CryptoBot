n =10;
r = 6;

c = linspace(0,r-1, r);
c_ini = c;
comb = c;
i = 1;
while i < length(c)
    if c(i) == c(i+1) - 1
        i = i + 1;
        if i == length(c)
            if c(i) < n - 1
                c(i) = c(i) + 1;
                i = i - 1;
                while i>0
                    c(i) = c_ini(i);
                    i = i - 1;
                end
                comb(end+1, :) = c(:);
                i = 1;
            end
        end

    else
        c(i) = c(i) + 1;
        i = i - 1;
        while i>0
            c(i) = c_ini(i);
            i = i - 1;
        end
        comb(end+1, :) = c(:);
        i = 1;
    end

end
