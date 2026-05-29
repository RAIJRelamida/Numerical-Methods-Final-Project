classdef RootsMethods

    methods

        function f = parse_function(~, expr)
            syms x
            f = matlabFunction(str2sym(expr));
        end

        function table = incremental(self, expr, x0, step, iterations)

            f = self.parse_function(expr);
            table = [];
            prev_x = NaN;

            for i = 1:iterations
                x1 = x0 + step;

                if isnan(prev_x)
                    error = 0;
                else
                    error = abs((x1 - prev_x)/x1)*100;
                end

                table = [table; i x0 x1 f(x0) f(x1) error];

                if f(x0)*f(x1) < 0
                    break;
                end

                prev_x = x1;
                x0 = x1;
            end
        end

        function table = bisection(self, expr, a, b, tol, max_iter)

            if nargin < 5, tol = 1e-6; end
            if nargin < 6, max_iter = 100; end

            f = self.parse_function(expr);
            table = [];
            prev_c = NaN;

            for i = 1:max_iter
                c = (a+b)/2;

                if isnan(prev_c)
                    error = 0;
                else
                    error = abs((c-prev_c)/c)*100;
                end

                table = [table; i a b c f(c) error];

                if abs(f(c)) < tol
                    break;
                end

                if f(a)*f(c) < 0
                    b = c;
                else
                    a = c;
                end

                prev_c = c;
            end
        end

        function table = regula_falsi(self, expr, a, b, tol, max_iter)

            if nargin < 5, tol = 1e-6; end
            if nargin < 6, max_iter = 100; end

            f = self.parse_function(expr);
            table = [];
            prev_c = NaN;

            for i = 1:max_iter

                c = (a*f(b) - b*f(a)) / (f(b) - f(a));

                if isnan(prev_c)
                    error = 0;
                else
                    error = abs((c-prev_c)/c)*100;
                end

                table = [table; i a b c f(c) error];

                if abs(f(c)) < tol
                    break;
                end

                if f(a)*f(c) < 0
                    b = c;
                else
                    a = c;
                end

                prev_c = c;
            end
        end

        function table = newton_raphson(self, expr, x0, tol, max_iter)

            if nargin < 4 || isempty(tol)
                tol = 1e-6;
            end
        
            if nargin < 5 || isempty(max_iter)
                max_iter = 100;
            end
        
            syms x
            f_expr = str2sym(expr);
            df_expr = diff(f_expr);
        
            f = matlabFunction(f_expr);
            df = matlabFunction(df_expr);
        
            table = [];
        
            for i = 1:max_iter
        
                if df(x0) == 0
                    error('Derivative became zero.');
                end
        
                x1 = x0 - f(x0)/df(x0);
        
                error_val = abs((x1-x0)/x1)*100;
        
                table = [table; i x0 x1 f(x1) error_val];
        
                if abs(f(x1)) < tol
                    break;
                end
        
                x0 = x1;
            end
        end

        function table = secant(self, expr, x0, x1, tol, max_iter)

            if nargin < 5, tol = 1e-6; end
            if nargin < 6, max_iter = 100; end

            f = self.parse_function(expr);
            table = [];

            for i = 1:max_iter

                x2 = x1 - (f(x1)*(x1-x0))/(f(x1)-f(x0));
                error = abs((x2-x1)/x2)*100;

                table = [table; i x0 x1 x2 f(x2) error];

                if abs(f(x2)) < tol
                    break;
                end

                x0 = x1;
                x1 = x2;
            end
        end
    end
end