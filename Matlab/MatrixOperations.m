classdef MatrixOperations

    methods

        function C = add(~, A, B)
            if ~isequal(size(A), size(B))
                error('Addition requires same dimensions');
            end
            C = A + B;
        end

        function C = multiply(~, A, B)
            if size(A,2) ~= size(B,1)
                error('Invalid multiplication dimensions');
            end
            C = A * B;
        end

        % TRANSPOSE
        function T = transpose(~, A)
            T = A.';   % Pure transpose
        end

        function d = determinant(~, A)
            if size(A,1) ~= size(A,2)
                error('Determinant requires square matrix');
            end
            d = det(A);
        end

        % INVERSE
        function invA = inverse(~, A)
            if size(A,1) ~= size(A,2)
                error('Inverse requires square matrix');
            end

            if abs(det(A)) < 1e-12
                error('Matrix is singular and cannot be inverted');
            end

            invA = inv(A);
        end

        % ADJOINT
        function adjA = adjoint(~, A)
            if size(A,1) ~= size(A,2)
                error('Adjoint requires square matrix');
            end

            d = det(A);

            if abs(d) < 1e-12
                error('Singular matrix');
            end

            adjA = d * inv(A);

            % Remove floating point errors
            adjA(abs(adjA) < 1e-10) = 0;
        end

        function P = power(~, A, n)
            if size(A,1) ~= size(A,2)
                error('Power requires square matrix');
            end
            P = A^n;
        end

        function X = solve_equations(~, A, B)
            if size(A,1) ~= size(A,2)
                error('A must be square');
            end
            X = A \ B;
        end
    end
end
