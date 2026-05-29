classdef MatrixUI < handle

    properties
        parentFig
        fig
        ops

        A_grid
        B_grid

        A_panel
        B_panel

        output

        % ================= MATRIX SIZE INPUTS =================
        rowsField
        colsField
    end

    methods

        % ================= CONSTRUCTOR =================
        function self = MatrixUI(parentFig, matrixOps)

            self.parentFig = parentFig;
            self.ops = matrixOps;

            self.fig = uifigure('Name','Matrix Calculator Pro', ...
                'Position',[200 100 1000 700]);

            self.build_ui();
        end

        % ================= CLOSE =================
        function go_back(self)
            close(self.fig);
        end

        % ================= READ MATRIX =================
        function M = read_matrix(~, grid)

            [r,c] = size(grid);

            M = zeros(r,c);

            for i = 1:r
                for j = 1:c
                    M(i,j) = grid(i,j).Value;
                end
            end
        end

        % ================= UI =================
        function build_ui(self)

            % ================= BACK =================
            uibutton(self.fig,'Text','Close', ...
                'Position',[10 650 100 30], ...
                'ButtonPushedFcn',@(s,e)self.go_back());

            % ================= TITLE =================
            uilabel(self.fig,'Text','Matrix Calculator Pro', ...
                'Position',[400 650 200 30], ...
                'FontSize',16);

            % ================= MATRIX SIZE INPUT =================
            uilabel(self.fig,'Text','Rows:', ...
                'Position',[50 600 50 25]);

            self.rowsField = uieditfield(self.fig,'numeric', ...
                'Position',[100 600 60 25], ...
                'Value',2);

            uilabel(self.fig,'Text','Cols:', ...
                'Position',[180 600 50 25]);

            self.colsField = uieditfield(self.fig,'numeric', ...
                'Position',[230 600 60 25], ...
                'Value',2);

            uibutton(self.fig,'Text','Set Size', ...
                'Position',[310 600 100 25], ...
                'ButtonPushedFcn',@(s,e)self.update_matrix_size());

            % ================= PANELS =================
            self.A_panel = uipanel(self.fig,'Title','Matrix A', ...
                'Position',[50 300 250 250]);

            self.B_panel = uipanel(self.fig,'Title','Matrix B', ...
                'Position',[350 300 250 250]);

            % DEFAULT GRID
            self.make_grid(self.A_panel,2,2,'A');
            self.make_grid(self.B_panel,2,2,'B');

            % ================= OUTPUT =================
            self.output = uitextarea(self.fig, ...
                'Position',[650 300 300 250]);

            % ================= BASIC OPS =================
            uibutton(self.fig,'Text','A + B', ...
                'Position',[650 250 100 30], ...
                'ButtonPushedFcn',@(s,e)self.add());

            uibutton(self.fig,'Text','A × B', ...
                'Position',[760 250 100 30], ...
                'ButtonPushedFcn',@(s,e)self.multiply());

            uibutton(self.fig,'Text','Solve Ax=B', ...
                'Position',[870 250 120 30], ...
                'ButtonPushedFcn',@(s,e)self.solve_eq());

            % ================= A OPERATIONS =================
            uibutton(self.fig,'Text','Transpose A', ...
                'Position',[650 210 120 30], ...
                'ButtonPushedFcn',@(s,e) ...
                self.unary(@(A) self.ops.transpose(A),'A'));

            uibutton(self.fig,'Text','Inverse A', ...
                'Position',[780 210 100 30], ...
                'ButtonPushedFcn',@(s,e) ...
                self.unary(@(A) self.ops.inverse(A),'A'));

            uibutton(self.fig,'Text','Det A', ...
                'Position',[890 210 80 30], ...
                'ButtonPushedFcn',@(s,e) ...
                self.unary(@(A) self.ops.determinant(A),'A'));

            uibutton(self.fig,'Text','Adj A', ...
                'Position',[650 170 100 30], ...
                'ButtonPushedFcn',@(s,e) ...
                self.unary(@(A) self.ops.adjoint(A),'A'));

            uibutton(self.fig,'Text','Power A', ...
                'Position',[760 170 100 30], ...
                'ButtonPushedFcn',@(s,e)self.power('A'));

            % ================= B OPERATIONS =================
            uibutton(self.fig,'Text','Transpose B', ...
                'Position',[650 130 120 30], ...
                'ButtonPushedFcn',@(s,e) ...
                self.unary(@(A) self.ops.transpose(A),'B'));

            uibutton(self.fig,'Text','Inverse B', ...
                'Position',[780 130 100 30], ...
                'ButtonPushedFcn',@(s,e) ...
                self.unary(@(A) self.ops.inverse(A),'B'));

            uibutton(self.fig,'Text','Det B', ...
                'Position',[890 130 80 30], ...
                'ButtonPushedFcn',@(s,e) ...
                self.unary(@(A) self.ops.determinant(A),'B'));

            uibutton(self.fig,'Text','Adj B', ...
                'Position',[650 90 100 30], ...
                'ButtonPushedFcn',@(s,e) ...
                self.unary(@(A) self.ops.adjoint(A),'B'));

            uibutton(self.fig,'Text','Power B', ...
                'Position',[760 90 100 30], ...
                'ButtonPushedFcn',@(s,e)self.power('B'));
        end

        % ================= UPDATE MATRIX SIZE =================
        function update_matrix_size(self)

            r = round(self.rowsField.Value);
            c = round(self.colsField.Value);

            if r <= 0 || c <= 0
                uialert(self.fig, ...
                    'Rows and Cols must be positive', ...
                    'Invalid Size');
                return;
            end

            self.make_grid(self.A_panel, r, c, 'A');
            self.make_grid(self.B_panel, r, c, 'B');
        end

        % ================= GRID =================
        function make_grid(self, panel, r, c, type)

            delete(panel.Children);

            grid = gobjects(r,c);

            startX = 20;
            startY = 200;

            boxW = 40;
            boxH = 30;

            spacing = 45;

            for i = 1:r
                for j = 1:c

                    x = startX + (j-1)*spacing;
                    y = startY - (i-1)*spacing;

                    grid(i,j) = uieditfield(panel,'numeric', ...
                        'Position',[x y boxW boxH], ...
                        'Value',0);
                end
            end

            % ================= STORE GRID =================
            if strcmp(type, 'A')
                self.A_grid = grid;
            else
                self.B_grid = grid;
            end
        end

        % ================= OUTPUT =================
        function show(self, R)

            % ================= NUMERIC OUTPUT =================
            if isnumeric(R)

                txt = evalc('disp(R)');

                self.output.Value = ...
                    splitlines(string(txt));

            % ================= TEXT OUTPUT =================
            else

                self.output.Value = ...
                    splitlines(string(R));
            end
        end

        % ================= BASIC OPS =================
        function add(self)

            A = self.read_matrix(self.A_grid);
            B = self.read_matrix(self.B_grid);

            try
                self.show(self.ops.add(A,B));

            catch ME
                self.show(ME.message);
            end
        end

        function multiply(self)

            A = self.read_matrix(self.A_grid);
            B = self.read_matrix(self.B_grid);

            try
                self.show(self.ops.multiply(A,B));

            catch ME
                self.show(ME.message);
            end
        end

        % ================= SOLVE AX = B =================
        function solve_eq(self)

            A = self.read_matrix(self.A_grid);
            B = self.read_matrix(self.B_grid);

            try

                X = self.ops.solve_equations(A,B);

                self.show(X);

            catch ME

                self.show(ME.message);
            end
        end

        % ================= UNARY OPS =================
        function unary(self, func, type)

            try

                if strcmp(type, 'A')

                    R = func( ...
                        self.read_matrix(self.A_grid));

                else

                    R = func( ...
                        self.read_matrix(self.B_grid));
                end

                self.show(R);

            catch ME

                self.show(ME.message);
            end
        end

        % ================= POWER =================
        function power(self, type)

            n = inputdlg('Enter power n:');

            if isempty(n)
                return;
            end

            n = str2double(n{1});

            try

                if strcmp(type, 'A')

                    R = self.ops.power( ...
                        self.read_matrix(self.A_grid), n);

                else

                    R = self.ops.power( ...
                        self.read_matrix(self.B_grid), n);
                end

                self.show(R);

            catch ME

                self.show(ME.message);
            end
        end
    end
end