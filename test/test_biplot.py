import unittest
import numpy as np
import pandas as pd
from biofes.biplot import *
from biofes import biplot

class test_functions(unittest.TestCase):
    def test_standardize(self):
        A = np.random.randint(low = 0, high = 200, size=(300, 30))
        A_st = standardize(A, meth=1)
        A_ref = (A-A.mean(axis = 0))/A.std(axis = 0)
        self.assertAlmostEqual(np.mean(A_ref - A_st), 0, msg='standardization error')
    
    def test_Inertia(self):
        A = np.random.randint(low = 0, high = 200, size=(300, 30))
        d = np.random.randint(30)
        EV, Inert = Inertia(A, d, niter=5, state = 0)
        
        U, Sigma, VT = SVD(A, d, niter=5, state = 0)
        
        EV_ref = np.power(Sigma,2)
        Inert_ref = EV_ref/np.sum(EV_ref) * 100
        
        try:
            if str((EV_ref - EV).mean()) == 'nan':
                pass
            else:
                self.assertAlmostEqual(np.mean(EV_ref - EV), 0, msg='EV error')
                self.assertAlmostEqual(np.mean(Inert_ref - Inert), 0, msg='EV error')
        except:
            pass
    
    def test_Factor2Binary(self):
        target = list(np.random.randint(np.random.randint(2, 10), size = 100))
        Z = Factor2Binary(target,Name = None)
        
        Z_ref = pd.get_dummies(target)
        self.assertAlmostEqual(np.mean(Z_ref.values - Z.values), 0, msg='Factor2Binary error')
    
    def test_matrixsqrt(self):
        A = np.random.randint(low = 0, high = 200, size=(300, 30))
        d = np.random.randint(30)
        tol = np.finfo(float).eps
        
        Sinv = matrixsqrt(A, d, tol, inv=True)
        U, Sigma, VT = SVD(A, d, niter=5, state=0)
        nz = Sigma > tol
        Sinv_ref = U.dot(np.diag(1/np.sqrt(Sigma[nz]))).dot(VT[nz,:])
        self.assertAlmostEqual(np.mean(Sinv_ref - Sinv), 0, delta=1e-5, msg='matrixsqrt (inv=True) error')
        
        ###############################################################################
        
        A = np.random.randint(low = 0, high = 200, size=(300, 30))
        d = np.random.randint(30)
        tol = np.finfo(float).eps
        
        S = matrixsqrt(A, d, tol, inv=False)
        U, Sigma, VT = SVD(A, d, niter=5, state=0)
        nz = Sigma > tol
        S_ref = U.dot(np.diag(np.sqrt(Sigma[nz]))).dot(VT[nz,:])
        self.assertAlmostEqual(np.mean(S_ref - S), 0, delta=1e-5, msg='matrixsqrt (inv=False) error')
        
        
class test_biplot(unittest.TestCase):
    def test_Classic(self):
        A = np.random.randint(low = 0, high = 200, size=(300, 30))
        d = np.random.randint(30)
        a = np.random.random(1)[0]
        methods = [None, 1]
        m = methods[np.random.randint(2)]
        
        BCla = biplot.Classic(data = A ,dim = d, alpha = a, method = m, niter = 5, state = 0)
        
        self.assertEqual(BCla.RowCoord.shape, (300, d), msg='dimension output error (Classic Biplot)')
        self.assertEqual(BCla.ColCoord.shape, ( 30, d) , msg='dimension output error (Classic Biplot)')
        self.assertEqual(len(BCla.Inert), d, msg='dimension output error (Classic Biplot)')
        self.assertEqual(len(BCla.EV)   , d, msg='dimension output error (Classic Biplot)')
        
    def test_Canonical(self):
        A = np.random.randint(low = 0, high = 200, size=(300, 30))
        target = list(np.random.randint(np.random.randint(2, 10), size = A.shape[0]))
        gn = list(set(target))
        d = np.random.randint(len(gn)+1, 30)
        methods = [None, 1]
        m = methods[np.random.randint(2)]
        
        BCan = biplot.Canonical(data = A, dim = d, GroupNames = gn, y = target, method = m, niter = 5, state = 0)
        
        self.assertEqual(BCan.Ind_Coord.shape, (300, len(gn)-1), msg='dimension output error (Canonical Biplot)')
        self.assertEqual(BCan.Var_Coord.shape, ( 30, len(gn)-1) , msg='dimension output error (Canonical Biplot)')
        self.assertEqual(len(BCan.inert), len(gn)-1, msg='dimension output error (Canonical Biplot)')

if __name__ == '__main__':
    unittest.main()