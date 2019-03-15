#! /usr/bin/env python3.4
import imageio
import numpy as np
from PIL import Image
from PIL import ImageDraw
from scipy.spatial import Delaunay
from scipy.interpolate import RectBivariateSpline
from scipy.ndimage.interpolation import map_coordinates


class Affine:
    def __init__(self, source, destination):
        if source.dtype.name != 'float64':
            raise ValueError("Source must be a 3x2 numpy array of float64")
        if destination.dtype.name != 'float64':
            raise ValueError("Destination must be a 3x2 numpy array of float64")
        if source.shape != (3, 2):
            raise ValueError("Shape should be a (3, 2)")
        if destination.shape != (3, 2):
            raise ValueError("Destination should be a (3, 2) array")

        self.source = source
        self.destination = destination

        A = np.float_([[self.source[0, 0], self.source[0, 1], 1, 0, 0, 0],
                       [0, 0, 0, self.source[0, 0], self.source[0, 1], 1],
                       [self.source[1, 0], self.source[1, 1], 1, 0, 0, 0],
                       [0, 0, 0, self.source[1, 0], self.source[1, 1], 1],
                       [self.source[2, 0], self.source[2, 1], 1, 0, 0, 0],
                       [0, 0, 0, self.source[2, 0], self.source[2, 1], 1]])

        B = np.float_([[self.destination[0, 0]],
                       [self.destination[0, 1]],
                       [self.destination[1, 0]],
                       [self.destination[1, 1]],
                       [self.destination[2, 0]],
                       [self.destination[2, 1]]])

        h = np.linalg.solve(A, B)
        self.matrix = np.float_([[h[0, 0], h[1, 0], h[2, 0]],
                                 [h[3, 0], h[4, 0], h[5, 0]],
                                 [0, 0, 1]])

    def transform(self, sourceImage, destinationImage):
        if not isinstance(sourceImage, np.ndarray):
            raise TypeError('SourceImage must be a numpy array')
        if not isinstance(destinationImage, np.ndarray):
            raise TypeError('destinationImage must be a numpy array')
        width = sourceImage.shape[1]
        height = sourceImage.shape[0]
        img = Image.new('L', (width, height), 0)
        vertices = [(self.destination[0][0], self.destination[0][1]), (self.destination[1][0],self.destination[1][1]), (self.destination[2][0], self.destination[2][1])]
        ImageDraw.Draw(img).polygon(vertices, outline=255, fill=255)
        mask = np.array(img)
        white = np.nonzero(mask)
        #approx = RectBivariateSpline(np.arange(sourceImage.shape[0]), np.arange(sourceImage.shape[1]), sourceImage, kx=1, ky=1)
        tempmat = np.vstack((list(white[1]), list(white[0]), np.ones(len(list(white[0])))))
        InvMatrix = np.linalg.inv(self.matrix)
        Coordinates = InvMatrix.dot(tempmat)
        #print(Coordinates[1], Coordinates[0])
        x = map_coordinates(sourceImage,[Coordinates[1], Coordinates[0]], order = 1, mode = 'nearest')
        destinationImage[list(white[0]),list(white[1])] = x

class Blender:
    def __init__(self, startImage, startPoints, endImage, endPoints):
        if not isinstance(startImage, np.ndarray):
            raise TypeError('startImage must be a numpy array')
        if type(startPoints) != np.ndarray:
            raise TypeError('startPoints must be a numpy array')
        if not isinstance(endImage, np.ndarray):
            raise TypeError('endImage must be a numpy array')
        if not isinstance(endPoints, np.ndarray):
            raise TypeError('endPoints must be a numpy array')
        self.startImage = startImage
        self.startPoints = startPoints
        self.endImage = endImage
        self.endPoints = endPoints

        self.tri = Delaunay(self.startPoints)

    def getBlendedImage(self, alpha):
        im0 = Image.new("L", (self.startImage.shape[1], self.startImage.shape[0]), "white")
        im1 = np.array(im0)
        im2 = np.array(im0)
        im4 = np.array(im0)
        for i in self.tri.simplices:
            A1 = np.float_([self.startPoints[i[0]],#[0], self.startPoints[i[0]][1]],
                            self.startPoints[i[1]],#[0], self.startPoints[i[1]][1]],
                            self.startPoints[i[2]]])#[0], self.startPoints[i[2]][1]]])
            A2 = np.float_([self.endPoints[i[0]],#[0], self.endPoints[i[0]][1]],
                            self.endPoints[i[1]],#[0], self.endPoints[i[1]][1]],
                            self.endPoints[i[2]]])#[0], self.endPoints[i[2]][1]]])
            A3 = np.float_(np.multiply(self.startPoints[i],(1- alpha)))
            A4 = np.float_(np.multiply(self.endPoints[i], (alpha)))
            targ = np.add(A3, A4)
            Af = Affine(A1, targ)
            Af.transform(self.startImage, im1)
            Af2 = Affine(A2, targ)
            Af2.transform(self.endImage, im2)
        im4[np.arange(self.startImage.shape[0])] = (1-alpha)*im1[np.arange(self.startImage.shape[0])]+alpha*im2[np.arange(self.startImage.shape[0])]
        #im3[np.arange(800)][np.arange(600)] = (1-alpha)*im1[np.arange(800)][np.arange(600)]+alpha*im2[np.arange(800)][np.arange(600)]
        temp1 = Image.fromarray(im4, 'L')
        temp1.show()
        J = alpha*100
        #temp1.save('Finals/{}Final.PNG'.format(round(J)), 'PNG')


        for i in range(self.startImage.shape[0]):
            for j in range(self.startImage.shape[1]):
                im4[i][j] = np.round((1-alpha)* im1[i][j]) + alpha*im2[i][j]

        return im4
 
class ColorAffine:
    def __init__(self, source, destination):
        if source.dtype.name != 'float64':
            raise ValueError("Source must be a 3x2 numpy array of float64")
        if destination.dtype.name != 'float64':
            raise ValueError("Destination must be a 3x2 numpy array of float64")
        if source.shape != (3, 2):
            raise ValueError("Shape should be a (3, 2)")
        if destination.shape != (3, 2):
            raise ValueError("Destination should be a (3, 2) array")

        self.source = source
        self.destination = destination

        A = np.float_([[self.source[0, 0], self.source[0, 1], 1, 0, 0, 0],
                       [0, 0, 0, self.source[0, 0], self.source[0, 1], 1],
                       [self.source[1, 0], self.source[1, 1], 1, 0, 0, 0],
                       [0, 0, 0, self.source[1, 0], self.source[1, 1], 1],
                       [self.source[2, 0], self.source[2, 1], 1, 0, 0, 0],
                       [0, 0, 0, self.source[2, 0], self.source[2, 1], 1]])

        B = np.float_([[self.destination[0, 0]],
                       [self.destination[0, 1]],
                       [self.destination[1, 0]],
                       [self.destination[1, 1]],
                       [self.destination[2, 0]],
                       [self.destination[2, 1]]])

        h = np.linalg.solve(A, B)
        self.matrix = np.float_([[h[0, 0], h[1, 0], h[2, 0]],
                                 [h[3, 0], h[4, 0], h[5, 0]],
                                 [0, 0, 1]])

    def transform(self, sourceImage, destinationImage):
        if not isinstance(sourceImage, np.ndarray):
            raise TypeError('SourceImage must be a numpy array')
        if not isinstance(destinationImage, np.ndarray):
            raise TypeError('destinationImage must be a numpy array')
        width = sourceImage.shape[1]
        height = sourceImage.shape[0]
        img = Image.new('L', (width, height), 0)
        vertices = [(self.destination[0][0], self.destination[0][1]), (self.destination[1][0],self.destination[1][1]), (self.destination[2][0], self.destination[2][1])]
        ImageDraw.Draw(img).polygon(vertices, outline='white', fill='white')
        mask = np.array(img)
        white = np.transpose(np.nonzero(mask))
        approx = RectBivariateSpline(np.arange(sourceImage.shape[0]), np.arange(sourceImage.shape[1]), sourceImage[:,:,0], kx=1, ky=1)
        approx1 = RectBivariateSpline(np.arange(sourceImage.shape[0]), np.arange(sourceImage.shape[1]), sourceImage[:,:,1], kx=1, ky=1)
        approx2 = RectBivariateSpline(np.arange(sourceImage.shape[0]), np.arange(sourceImage.shape[1]), sourceImage[:,:,2], kx=1, ky=1)
        for i in white:
            tempmat = np.float_([[i[1]],
                                 [i[0]],
                                 [1]])
            Coordinates = np.matmul(np.linalg.inv(self.matrix), tempmat)
            pixel = approx.ev(Coordinates[1], Coordinates[0])
            pixel1 = approx1.ev(Coordinates[1], Coordinates[0])
            pixel2 = approx2.ev(Coordinates[1], Coordinates[0])
            destinationImage[i[0]][i[1]] = [pixel,pixel1,pixel2]
        '''
        white = np.nonzero(mask)
        #approx = RectBivariateSpline(np.arange(sourceImage.shape[0]), np.arange(sourceImage.shape[1]), sourceImage, kx=1, ky=1)
        tempmat = np.vstack((list(white[1]), list(white[0]), np.ones(len(list(white[0])))))
        InvMatrix = np.linalg.inv(self.matrix)
        Coordinates = InvMatrix.dot(tempmat)
        #print(Coordinates[1], Coordinates[0])
        #print(sourceImage[0][0])
        
        x = map_coordinates(sourceImage,[Coordinates[1], Coordinates[0]], order = 1, mode = 'nearest')
        destinationImage[list(white[0]),list(white[1])] = x
        
        
        #x = map_coordinates(sourceImage,[Coordinates[1],Coordinates[0]], order = 1, mode = 'nearest')
        #print(x)
        #destinationImage[list(white[0]),list(white[1])] = x#,[list(white[0]),list(white[1])]] = x
        '''

class ColorBlender:
    def __init__(self, startImage, startPoints, endImage, endPoints):
        if not isinstance(startImage, np.ndarray):
            raise TypeError('startImage must be a numpy array')
        if type(startPoints) != np.ndarray:
            raise TypeError('startPoints must be a numpy array')
        if not isinstance(endImage, np.ndarray):
            raise TypeError('endImage must be a numpy array')
        if not isinstance(endPoints, np.ndarray):
            raise TypeError('endPoints must be a numpy array')
        self.startImage = startImage
        self.startPoints = startPoints
        self.endImage = endImage
        self.endPoints = endPoints
        self.tri = Delaunay(self.startPoints)

    def getBlendedImage(self, alpha):
        im0 = Image.new("RGB", (self.startImage.shape[1], self.startImage.shape[0]), "white")
        im1 = np.array(im0)
        im2 = np.array(im0)
        im4 = np.array(im0)
        for i in self.tri.simplices:
            A1 = np.float_([self.startPoints[i[0]],#[0], self.startPoints[i[0]][1]],
                            self.startPoints[i[1]],#[0], self.startPoints[i[1]][1]],
                            self.startPoints[i[2]]])#[0], self.startPoints[i[2]][1]]])
            A2 = np.float_([self.endPoints[i[0]],#[0], self.endPoints[i[0]][1]],
                            self.endPoints[i[1]],#[0], self.endPoints[i[1]][1]],
                            self.endPoints[i[2]]])#[0], self.endPoints[i[2]][1]]])
            A3 = np.float_(np.multiply(self.startPoints[i],(1- alpha)))
            A4 = np.float_(np.multiply(self.endPoints[i], (alpha)))
            targ = np.add(A3, A4)
            Af = ColorAffine(A1, targ)
            Af.transform(self.startImage, im1)
            Af2 = ColorAffine(A2, targ)
            Af2.transform(self.endImage, im2)
        
        im4[np.arange(self.startImage.shape[0])] = (1-alpha)*im1[np.arange(self.startImage.shape[0])]+alpha*im2[np.arange(self.startImage.shape[0])]
        #im3[np.arange(800)][np.arange(600)] = (1-alpha)*im1[np.arange(800)][np.arange(600)]+alpha*im2[np.arange(800)][np.arange(600)]
        temp1 = Image.fromarray(im4, 'RGB')
        temp1.show()
        J = alpha*100
        #temp1.save('Finals/{}Final.PNG'.format(round(J)), 'PNG')


        for i in range(self.startImage.shape[0]):
            for j in range(self.startImage.shape[1]):
                im4[i][j] = np.round((1-alpha)* im1[i][j]) + alpha*im2[i][j]

        return im4

if __name__ == "__main__":
    '''
    compare = imageio.imread('test_data/Alpha50Gray.png')
    startPoint = np.load('test_data/startPoints.npy')
    endPoint = np.load('test_data/endPoints.npy')
    startImage = imageio.imread('test_data/StartSmallGray.png')
    endImage = imageio.imread('test_data/EndSmallGray.png')
    blend = Blender(startImage, startPoint, endImage, endPoint)
    A = blend.getBlendedImage(.5)
    count = 0
    for i in range(300):
        for j in range(400):
            diff = int(compare[i][j]) - int(A[i][j])
            if diff > 5 or diff < -5:
                count = count+1
                print(i,j,diff)
    print(count)
    temp = Image.fromarray(A, 'L')
    temp.show()

'''
    startPoints = np.loadtxt('tiger2.jpg.txt')
    endPoints = np.loadtxt('wolf.jpg.txt')
    startImage = imageio.imread('Tiger2Gray.jpg')
    endImage = imageio.imread('WolfGray.jpg')
    B = Blender(startImage, startPoints, endImage, endPoints)
    '''
    i = 0
    while i < 1.01:
        final = B.getBlendedImage(i)
        i += .05
    '''
    startImage2 = imageio.imread('Tiger2Color.jpg')
    endImage2 = imageio.imread('WolfColor.jpg')
    B = ColorBlender(startImage2, startPoints, endImage2, endPoints)
    i = 0
    final = B.getBlendedImage(0.5)
    '''
    while i < 1.01:
        final = B.getBlendedImage(i)
        i += .05
    '''
