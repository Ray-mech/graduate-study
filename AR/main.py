from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import cv2
import cv2.aruco as aruco
import numpy as np
from PIL import Image


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Indicator_for_CGR")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape) 
    init(640, 480)
    glutMainLoop()


def init(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_ALPHA_TEST);
    
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # prepare textures
    texture_background = glGenTextures(1)
    texture_obj = glGenTextures(1)
    
    # background texture
    frame, rvecs, tvecs = detect()
    bg_image = cv2.flip(frame, 0)
    bg_image = Image.fromarray(bg_image)     
    ix = bg_image.size[0]
    iy = bg_image.size[1]
    bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
    
    # object texture
    ob_image = cv2.imread("./potd.png")
    """cv2.imshow("a",ob_image)""" # just for confirmation
    ob_image = cv2.flip(ob_image, 0)
    ob_image = Image.fromarray(ob_image)     
    ix2 = ob_image.size[0]
    iy2 = ob_image.size[1]
    ob_image = ob_image.tobytes("raw", "BGRX", 0, -1)
    glBindTexture(GL_TEXTURE_2D, texture_obj)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix2, iy2, 0, GL_RGBA, GL_UNSIGNED_BYTE, ob_image)
    
    # draw
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glTranslatef(0.0,0.0,-7.3)
    _draw_background()
    glPopMatrix()
    
    if (rvecs != []): #detected
        vmat = makematrix(rvecs, tvecs)
        glLoadMatrixd(vmat)
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, texture_obj)
        _draw_object()
        glPopMatrix()
 
    glutSwapBuffers()
    glutPostRedisplay()
    
    
def _draw_background():
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd( )
        
def _draw_object():
        s = 0.045
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-5*s, -2*s, 0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 5*s, -2*s, 0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 5*s,  2*s, 0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-5*s,  2*s, 0)
        glEnd( )
        
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    
def detect():
    # camera: c270
    cameraMatrix = np.array([[8.2177218160147447e+02, 0.0                   , 3.4694289806342221e+02],
                             [0.0                   , 8.2177218160147447e+02, 2.4795144956871457e+02],
                             [0.0                   , 0.0                   , 1.0                   ]])
    distCoeffs = np.array([4.4824308523616324e-02, -7.4951985348854000e-01, 3.7539708742088725e-03, 8.8931335565222442e-03, 3.7214188475390984e+00])

    rvecs = np.array([])
    tvecs = np.array([])
    
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if (corners != []): 
        rvecs, tvecs = aruco.estimatePoseSingleMarkers(corners, 0.05, cameraMatrix, distCoeffs)
        """
        frame = aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvecs, tvecs, 0.1)
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        """
        
    return frame, rvecs, tvecs


def makematrix(rvecs, tvecs):
    rmtx = cv2.Rodrigues(rvecs[0][0])[0]

    view_matrix = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0][0][0]],
                            [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[0][0][1]],
                            [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvecs[0][0][2]],
                            [0.0       ,0.0       ,0.0       ,1.0    ]])
 
    inverse_matrix = np.array([[ 1.0, 1.0, 1.0, 1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [ 1.0, 1.0, 1.0, 1.0]])
 
    view_matrix = view_matrix * inverse_matrix
    view_matrix = np.transpose(view_matrix)

    return view_matrix
    

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    main()
