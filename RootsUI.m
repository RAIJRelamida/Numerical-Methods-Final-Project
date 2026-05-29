classdef RootsUI < handle

    properties
        fig
        ax
        exprField
        tableUI
        backCallback
        currentExpr

        % ================= USER INPUT FIELDS =================
        xlField
        xuField
    end

    methods

        function self = RootsUI(backCallback, ~)

            self.backCallback = backCallback;

            self.fig = uifigure('Name','Root Solver', ...
                'Position',[200 100 1000 650]);

            self.build_fx_screen();
        end

        % ================= INPUT SCREEN =================
        function build_fx_screen(self)

            delete(self.fig.Children);

            % ================= FUNCTION INPUT =================
            uilabel(self.fig,'Text','Enter f(x) =', ...
                'Position',[20 600 100 30]);

            self.exprField = uieditfield(self.fig,'text', ...
                'Position',[120 600 350 30]);

            % ================= XL INPUT =================
            uilabel(self.fig,'Text','XL / x0:', ...
                'Position',[500 600 70 30]);

            self.xlField = uieditfield(self.fig,'numeric', ...
                'Position',[570 600 80 30], ...
                'Value',1);

            % ================= XU INPUT =================
            uilabel(self.fig,'Text','XU / x1:', ...
                'Position',[670 600 70 30]);

            self.xuField = uieditfield(self.fig,'numeric', ...
                'Position',[740 600 80 30], ...
                'Value',2);

            % ================= BUTTONS =================
            uibutton(self.fig,'Text','Incremental', ...
                'Position',[20 540 120 30], ...
                'ButtonPushedFcn',@(s,e)self.run_solver("Incremental"));

            uibutton(self.fig,'Text','Bisection', ...
                'Position',[150 540 120 30], ...
                'ButtonPushedFcn',@(s,e)self.run_solver("Bisection"));

            uibutton(self.fig,'Text','Regula Falsi', ...
                'Position',[280 540 120 30], ...
                'ButtonPushedFcn',@(s,e)self.run_solver("Regula Falsi"));

            uibutton(self.fig,'Text','Newton-Raphson', ...
                'Position',[410 540 140 30], ...
                'ButtonPushedFcn',@(s,e)self.run_solver("Newton-Raphson"));

            uibutton(self.fig,'Text','Secant', ...
                'Position',[560 540 120 30], ...
                'ButtonPushedFcn',@(s,e)self.run_solver("Secant"));

            uibutton(self.fig,'Text','← Back', ...
                'Position',[700 540 120 30], ...
                'ButtonPushedFcn',@(s,e)self.close_to_main());

            % ================= GRAPH =================
            self.ax = uiaxes(self.fig,'Position',[30 80 600 420]);

            grid(self.ax,'on');
            hold(self.ax,'on');

            % ================= TABLE =================
            self.tableUI = uitable(self.fig, ...
                'Position',[650 80 320 420], ...
                'ColumnName',{}, ...
                'Data',{});
        end

        % ================= BACK =================
        function close_to_main(self)

            delete(self.fig);

            if ~isempty(self.backCallback)
                self.backCallback();
            end
        end

        % ================= SOLVER =================
        function run_solver(self, method)

            expr = self.exprField.Value;

            if isempty(expr)
                uialert(self.fig,'Enter f(x)','Missing Input');
                return;
            end

            self.currentExpr = expr;

            self.show_results(method);
        end

        % ================= RESULTS =================
        function show_results(self, method)

            try

                syms x

                f_sym = str2sym(self.currentExpr);

                f = matlabFunction(f_sym);

                df = matlabFunction(diff(f_sym));

                % ================= RESET AXES =================
                cla(self.ax,'reset');

                hold(self.ax,'on');


                x_vals = linspace(-10,10,400);

                y_vals = arrayfun(@(t) f(t), x_vals);

                plot(self.ax, x_vals, y_vals, ...
                    'b', 'LineWidth', 2);

                yline(self.ax,0,'r');

                tableData = [];

                colNames = ...
                    {'Iter','XL','XU','XR','f(XR)','Error %'};

                switch method


                    % INCREMENTAL METHOD

                    case "Incremental"

                        xl = self.xlField.Value;
                        step = self.xuField.Value;

                        prev_xr = NaN;

                        for i = 1:10

                            xu = xl + step;

                            xr = xu;

                            if isnan(prev_xr)
                                err = 0;
                            else
                                err = abs((xr-prev_xr)/xr)*100;
                            end

                            plot(self.ax,xr,f(xr), ...
                                'ks','MarkerFaceColor','y');

                            tableData = [tableData;
                                i xl xu xr f(xr) err];

                            if f(xl)*f(xu) < 0
                                break;
                            end

                            prev_xr = xr;

                            xl = xu;
                        end


                    % BISECTION METHOD

                    case "Bisection"

                        xl = self.xlField.Value;
                        xu = self.xuField.Value;

                        prev_xr = NaN;

                        for i = 1:10

                            xr = (xl+xu)/2;

                            if isnan(prev_xr)
                                err = 0;
                            else
                                err = abs((xr-prev_xr)/xr)*100;
                            end

                            plot(self.ax,xr,f(xr), ...
                                'ro','MarkerFaceColor','r');

                            tableData = [tableData;
                                i xl xu xr f(xr) err];

                            if f(xl)*f(xr) < 0
                                xu = xr;
                            else
                                xl = xr;
                            end

                            prev_xr = xr;
                        end

                    % REGULA FALSI METHOD

                    case "Regula Falsi"

                        xl = self.xlField.Value;
                        xu = self.xuField.Value;

                        prev_xr = NaN;

                        for i = 1:10

                            xr = (xl*f(xu)-xu*f(xl)) / ...
                                 (f(xu)-f(xl));

                            if isnan(prev_xr)
                                err = 0;
                            else
                                err = abs((xr-prev_xr)/xr)*100;
                            end

                            plot(self.ax,xr,f(xr), ...
                                'go','MarkerFaceColor','g');

                            tableData = [tableData;
                                i xl xu xr f(xr) err];

                            if f(xl)*f(xr) < 0
                                xu = xr;
                            else
                                xl = xr;
                            end

                            prev_xr = xr;
                        end


                    % NEWTON RAPHSON METHOD

                    case "Newton-Raphson"

                        xi = self.xlField.Value;

                        for i = 1:10

                            xr = xi - f(xi)/df(xi);

                            err = abs((xr-xi)/xr)*100;

                            plot(self.ax,xr,f(xr), ...
                                'bo','MarkerFaceColor','b');

                            tableData = [tableData;
                                i xi NaN xr f(xr) err];

                            xi = xr;
                        end


                    % SECANT METHOD

                    case "Secant"

                        xl = self.xlField.Value;
                        xu = self.xuField.Value;

                        for i = 1:10

                            xr = xu - ...
                                (f(xu)*(xu-xl)) / ...
                                (f(xu)-f(xl));

                            err = abs((xr-xu)/xr)*100;

                            plot(self.ax,xr,f(xr), ...
                                'mo','MarkerFaceColor','m');

                            tableData = [tableData;
                                i xl xu xr f(xr) err];

                            xl = xu;

                            xu = xr;
                        end
                end

                % ================= UPDATE TABLE =================
                self.tableUI.Data = tableData;

                self.tableUI.ColumnName = colNames;

                title(self.ax, method);

                drawnow;

                hold(self.ax,'off');

            catch ME

                uialert(self.fig, ...
                    ME.message, ...
                    'Solver Error');
            end
        end
    end
end