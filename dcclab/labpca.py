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
        """The reconstructed spectrum from the principal components, and the residuals

        The pca transform method will return the coefficients in the centered spectral
        space.  Sometimes, we want to compare the actual reconstructed spectrum with
        its original version to see how well the PCs can model the spectrum.

        Here we do so for a set of spectra and return the reconstructed spectra and
        their residuals.
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

    def recover_concentrations_independently(self, S, A):
        """Using the principal components space, we model spectra S and A, then
        use a projection to recover the concentration.

        S is a set of (samples) spectra from which we are interested in extracting the concentration of W
        A is a set of (analytes) spectra of which we want to know the concentration
        """

        a_ap = self.transform(A)
        s_ip = self.transform(S)
        approx_analytes = a_ap @ self.components_ + self.mean_
        approx_samples = s_ip @ self.components_ + self.mean_
        recoveredConcentrations_ai = approx_analytes @ approx_samples.T

        analytes_residuals = A - approx_analytes

        return recoveredConcentrations_ai, approx_analytes, analytes_residuals

    def recover_concentrations_fit(self, S, A):
        """Using the principal components space, we model spectra S and A, then
        use a projection to recover the concentration.

        S is a set of (samples) spectra from which we are interested in extracting the concentration of W
        A is a set of (analytes) spectra of which we want to know the concentration
        """

        a_ap = self.transform_noncentered(A)
        s_ip = self.transform_noncentered(S)

        invb_ap = np.linalg.pinv(a_ap).T

        recoveredConcentrations_ai = invb_ap @ s_ip.T

        approx_analytes = a_ap @ self.components_ + self.mean_
        approx_samples = s_ip @ self.components_ + self.mean_

        analytes_residuals = A - approx_analytes

        return recoveredConcentrations_ai, approx_analytes, analytes_residuals


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def createComponent(x, maxPeaks, maxAmplitude, maxWidth, minWidth):
        N = random.randint(1, maxPeaks)

        intensity = np.zeros(len(x))
        for i in range(N):
            amplitude = random.uniform(0, maxAmplitude)
            width = random.uniform(minWidth, maxWidth)
            center = random.choice(x)
            intensity += amplitude * np.exp(-((x - center) ** 2) / width**2)

        intensity /= np.sqrt(intensity @ intensity)
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
    basis_set = createBasisSet(x=X, N=5, maxPeaks=5)
    data_set, concentrations = createDatasetFromBasisSet(100, basis_set)

    """ Analysis is as usual with PCA """
    pca = LabPCA(n_components=5)
    pca.fit(data_set)

    """ Here is an example: you want to know the concentration of the first 3 basis_set 
    in the spectrum data_set """
    which = list((0, 1, 2))
    known_analyte_spectrum = basis_set[which]

    (
        recovered_concentrations_ind,
        approx_spectra,
        residuals,
    ) = pca.recover_concentrations_independently(data_set, known_analyte_spectrum)

    (
        recovered_concentrations_fit,
        approx_spectra,
        residuals,
    ) = pca.recover_concentrations_fit(data_set, known_analyte_spectrum)

    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.set_size_inches(8, 11)
    fig.tight_layout(pad=5.0)

    ax1.plot(basis_set.T, linewidth=1)
    ax1.text(
        0.1,
        0.7,
        "Analytes used to produced spectra.\nOrthogonal when they do not overlap.\nOverlap will make recovery inaccurate",
        transform=ax1.transAxes,
    )
    ax1.set_title("Basis analytes")
    ax1.set_xlabel("Frequency")
    ax1.set_ylabel("Relative intensity")
    ax2.plot(
        concentrations[which].T,
        recovered_concentrations_ind[which].T,
        marker="o",
        linewidth=0,
    )
    ax2.text(
        0.4,
        0.1,
        "Each analyte is projected onto the spectrum\nin the principal components basis.\nLess acurate.",
        transform=ax2.transAxes,
    )
    ax2.set_title("Accuracy of concentration recovery (independently)")
    ax2.set_xlabel("Actual concentration")
    ax2.set_ylabel("Recovered concentration")
    ax2.set_ylim(0, 1.2)
    ax3.plot(
        concentrations[which].T,
        recovered_concentrations_fit[which].T,
        marker="o",
        linewidth=0,
    )
    ax3.text(
        0.4,
        0.1,
        "All analytes projected onto the spectrum in the principal\ncomponents basis as a group to minimize error.\nMore acurate.",
        transform=ax3.transAxes,
    )
    ax3.set_title("Accuracy of concentration recovery (as a group) via fit")
    ax3.set_xlabel("Actual concentration")
    ax3.set_ylabel("Recovered concentration")
    ax3.set_ylim(0, 1.2)
    plt.show()
