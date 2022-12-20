import numpy as np
from sklearn.decomposition import PCA
import random


class LabPCA(PCA):
    """An extension of the sklearn.PCA class that manipulates the values
    of pca coefficients to allow for reconstructed vectors to be similar
    to the original (i.e. without centering) and allows concentration
    extraction for an arbitrary spectrum.
    """

    def transform_noncentered(self, X):
        """The coefficients in non-centered PCA space

        The PCA.transform method subtracts the average of all spectra
        before doing its pca.  Therefore, the coefficients correspond
        to the centered spectra, which is not always what we want.
        For instance, to recover concentrations, we need to have the
        non-centered pca coefficients to express a spectrum as a sum of
        other spectra. If you were to transform the average spectrum,
        you would get all coefficients to be zero.  To recover the
        (opposite of) coefficients that correspond to the mean, we need
        to transform a null spectrum, which will give us the opposite
        of the average spectrum coefficient.
        """
        originCoefficients = np.zeros(shape=X.shape)
        return self.transform(X) + (-self.transform(originCoefficients))

    def approximate_spectrum(self, A):
        """The reconstructed spectrum from the principal components and the residuals

        The pca transform method will return the coefficients in the centered spectral
        space.  Sometimes, we want to compare the actual reconstructed spectrum with
        its original version to see how well the PCs can model the spectrum.

        Here we do so for a set of spectra and return the reconstructed spectra and
        the residuals.
        """
        a_ap = self.transform_noncentered(A)
        approx_spectra = x_ap @ self.components_
        residuals = A - approx_sectra
        return approx_spectra, residuals

    @property
    def components_noncentered_(self):
        """The non-centered components

        The components_ are the deviations from the average spectrum and
        therefore always oscillate around 0.  By adding the mean_ spectrum
        we get the actual shape of the principal components.
        """

        return self.components_ + self.mean_

    def recover_concentration(self, S, A):
        """Using the principal components space, we model spectra S and A, then
        use a projection to recover the concentration.

        S is a set of (samples) spectra from which we are interested in extracting the concentration of W
        A is a set of (analytes) spectra of which we want to know the concentration
        """
        a_ap = self.transform_noncentered(A)
        s_pi = self.transform_noncentered(S).T
        invb_ap = np.linalg.pinv(a_ap).T
        approx_spectra = a_ap @ self.components_

        recoveredConcentrations_ki = (invb_ap @ s_pi).T
        spectral_residuals = A - approx_spectra

        return recoveredConcentrations_ki, approx_spectra, spectral_residuals


if __name__ == "__main__":

    def createComponent(x, maxPeaks, maxAmplitude, maxWidth, minWidth):
        N = random.randint(1, maxPeaks)

        intensity = np.zeros(len(x))
        for i in range(N):
            amplitude = random.uniform(0, maxAmplitude)
            width = random.uniform(minWidth, maxWidth)
            center = random.choice(x)
            intensity += amplitude * np.exp(-((x - center) ** 2) / width**2)

        return intensity

    def createBasisSet(x, N, maxPeaks=5, maxAmplitude=1, maxWidth=30, minWidth=5):
        basisSet = []
        for i in range(N):
            component = createComponent(x, maxPeaks, maxAmplitude, maxWidth, minWidth)
            basisSet.append(component)

        return np.array(basisSet)

    def createDatasetFromBasisSet(N, basisSet):
        m, nPts = basisSet.shape
        C = np.random.rand(m, N)

        return (basisSet.T @ C).T, C

    """ Create test data """
    X = np.linspace(0, 1000, 1001)
    basis_set = createBasisSet(x=X, N=5)
    data_set, concentrations = createDatasetFromBasisSet(100, basis_set)

    """ Analysis is as usual with PCA """
    pca = LabPCA(n_components=5)
    pca.fit(data_set)

    print(data_set.shape)
    print(basis_set.shape)

    """ Here is an example: you want to know the concentration of basis_set[0] 
    in the spectrum data_set[10] """
    known_analyte_spectrum = basis_set[0].reshape(1,-1)
    print(known_analyte_spectrum.shape)
    recovered_concentrations, approx_spectra, residuals = pca.recover_concentration(
        data_set, known_analyte_spectrum
    )
    print(concentrations.T)
    print(recovered_concentrations)
