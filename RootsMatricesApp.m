classdef RootsMatricesApp < handle

    properties
        fig
        rootsMethods
        matrixOps
    end

    methods
        function self = RootsMatricesApp()

            self.fig = uifigure('Name','Roots and Matrices Solver', ...
                                'Position',[100 100 1000 700], ...
                                'Color',[0.1 0.1 0.1]);

            self.rootsMethods = RootsMethods();
            self.matrixOps = MatrixOperations();

            self.create_main_menu();
        end

        function create_main_menu(self)

            clf(self.fig);

            uilabel(self.fig, ...
                'Text','Roots and Matrices Solver', ...
                'FontSize',28, ...
                'FontWeight','bold', ...
                'Position',[300 600 500 50], ...
                'FontColor','white');

            uilabel(self.fig, ...
                'Text','Numerical Methods and Linear Algebra', ...
                'Position',[360 560 400 30], ...
                'FontColor',[0.8 0.8 0.8]);

            uibutton(self.fig,'Text','Find Roots', ...
                'Position',[400 450 200 50], ...
                'ButtonPushedFcn',@(s,e)self.open_roots());

            uibutton(self.fig,'Text','Matrix Calculator', ...
                'Position',[400 380 200 50], ...
                'ButtonPushedFcn',@(s,e)self.open_matrix());

            uibutton(self.fig,'Text','Exit', ...
                'Position',[430 300 140 40], ...
                'ButtonPushedFcn',@(s,e)close(self.fig));
        end

        % ================= ROOTS OPEN =================
        function open_roots(self)
            RootsUI(@self.create_main_menu, self.rootsMethods);
        end

        function open_matrix(self)
            MatrixUI(self.fig, self.matrixOps);
        end
    end
end