import numpy as np
from PIL import Image
from scipy.signal import convolve2d
class featuremap_read:
    def __init__(self, data=None, range=None, tag=None, sorce_data=None, label_data=None):
        self.data = data
        self.range = range
        self.tag = tag
        self.sorce = sorce_data
        self.label = label_data
    def get_data(self):
        if self.data:
            result = []
            _data = self.data
            img_len = len(_data[0]['value'])
            over_len = img_len - (self.range+16)
            if over_len >= 0:
                values = {'wall_time': _data[0]['wall_time'],
                          'step': _data[0]['step'],
                          'Remaining_pictures': over_len,
                          'value':  _data[0]['value'][self.range:(self.range+16), :, :],
                          'sorce_data': self.sorce[0]['value'].tolist()
                          }


            else:
                values = {'wall_time': _data[0]['wall_time'],
                          'step': _data[0]['step'],
                          'Remaining_pictures': 0,
                          'value': _data[0]['value'][self.range:, :, :],
                          'sorce_data': self.sorce[0]['value'].tolist()
                          }
            if self.label:
                values["label"] = self.label[0]['value'].tolist()
            result.append(values)
            return result
        else:
            return None

class featuremap_diff_read:
    def __init__(self, data1=None, data2=None):
        self.data1 = data1
        self.data2 = data2

    def get_data(self):
        max_diff = 1
        data1 = self.data1[0]['value']
        data2 = self.data2[0]['value']
        for img1, img2 in zip(data1, data2):
            gray1 = 0.3*img1[0] + 0.59*img1[1] + 0.11*img1[2]
            gray2 = 0.3 * img2[0] + 0.59 * img2[1] + 0.11 * img2[2]
            diff_data = self.compute_ssim(gray1, gray2)
            if diff_data < max_diff:
                max_diff = diff_data
        return max_diff



    def matlab_style_gauss2D(self, shape=(3, 3), sigma=0.5):
        """
        2D gaussian mask - should give the same result as MATLAB's
        fspecial('gaussian',[shape],[sigma])
        """
        m, n = [(ss - 1.) / 2. for ss in shape]
        y, x = np.ogrid[-m:m + 1, -n:n + 1]
        h = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
        h[h < np.finfo(h.dtype).eps * h.max()] = 0
        sumh = h.sum()
        if sumh != 0:
            h /= sumh
        return h


    def filter2(self, x, kernel, mode='same'):
        return convolve2d(x, np.rot90(kernel, 2))


    def compute_ssim(self, im1, im2, k1=0.01, k2=0.03, win_size=11, L=255):
        if not im1.shape == im2.shape:
            raise ValueError("Input Imagees must have the same dimensions")
        if len(im1.shape) > 2:
            raise ValueError("Please input the images with 1 channel")

        M, N = im1.shape
        C1 = (k1 * L) ** 2
        C2 = (k2 * L) ** 2
        window = self.matlab_style_gauss2D(shape=(win_size, win_size), sigma=1.5)
        window = window / np.sum(np.sum(window))

        if im1.dtype == np.uint8:
            im1 = np.double(im1)
        if im2.dtype == np.uint8:
            im2 = np.double(im2)

        mu1 = self.filter2(im1, window, 'valid')
        mu2 = self.filter2(im2, window, 'valid')
        mu1_sq = mu1 * mu1
        mu2_sq = mu2 * mu2
        mu1_mu2 = mu1 * mu2
        sigma1_sq = self.filter2(im1 * im1, window, 'valid') - mu1_sq
        sigma2_sq = self.filter2(im2 * im2, window, 'valid') - mu2_sq
        sigmal2 = self.filter2(im1 * im2, window, 'valid') - mu1_mu2

        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigmal2 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

        return np.mean(np.mean(ssim_map))

