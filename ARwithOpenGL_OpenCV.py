from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import cv2
import cv2.aruco as aruco
import numpy as np
from PIL import Image


cap = cv2.VideoCapture(0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"openglTest")      # show window
    glutDisplayFunc(display2)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    init(640, 480)
    glutMainLoop()

def init(width, height):
    """ initialize """
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST) # enable shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    ##set perspective
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glEnable(GL_TEXTURE_2D)
    texture_background = glGenTextures(1)
    texture_cube = glGenTextures(1)
def display2():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    texture_background = glGenTextures(1)
    texture_obj = glGenTextures(1)
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
    
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
     
    # draw background
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glPushMatrix()
    glTranslatef(0.0,0.0,-7.3)

    _draw_background()
    glPopMatrix()
    
    if (rvecs != []):
        vmat = makematrix(rvecs, tvecs)
        glLoadMatrixd(vmat)
        glColor3f(1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, texture_obj)
        glutWireTeapot(0.1)   # wireframe
        #glutSolidTeapot(0.1)  # solid
        glPushMatrix()
        glPopMatrix()
    #glPopMatrix()
    
    # handle glyph
    #image = self._handle_glyph(image)
 
    glutSwapBuffers()
    glutPostRedisplay()
def _draw_background():
        # draw background
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd( )
        
def display():
    #print(time.time())
    """ display """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    ##set camera


    #ret, frame = cap.read()
    frame, rvecs, tvecs = detect()
    frame = cv2.flip(frame, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #print(rvecs,"---------------------------\n")



    glDrawPixels(640, 480,GL_RGB, GL_UNSIGNED_BYTE, np.ascontiguousarray(frame.data))
    glClear(GL_DEPTH_BUFFER_BIT)
    if (rvecs != []):
        
        #print(rvecs[0][0][0])
        #gluLookAt(0.0, 1.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        #gluLookAt(0,1,5,tvecs[0][0][0],tvecs[0][0][1],tvecs[0][0][2], 0.0, 1.0, 0.0)
        vmat = makematrix(rvecs, tvecs)
        print(vmat)
        glPushMatrix()
        glLoadMatrixd(vmat)
        glPopMatrix()
        #gluLookAt(vmat)
        ##draw a teapot
        glColor3f(1.0, 0.0, 0.0)
        glutWireTeapot(0.8)   # wireframe
        #glutSolidTeapot(1.0)  # solid
    glFlush()  # enforce OpenGL command
    glutPostRedisplay()

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    
def detect():
    cameraMatrix = np.array([[8.2177218160147447e+02, 0., 3.4694289806342221e+02],[0., 8.2177218160147447e+02, 2.4795144956871457e+02],[0., 0., 1.]])
    distCoeffs = np.array([4.4824308523616324e-02, -7.4951985348854000e-01, 3.7539708742088725e-03, 8.8931335565222442e-03, 3.7214188475390984e+00])
    #型宣言
    rvecs = np.array([])
    tvecs = np.array([])
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    #print(parameters)
 
    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    #print(corners)
 
    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs

    if (corners != []): 
        rvecs, tvecs = aruco.estimatePoseSingleMarkers(corners, 0.05, cameraMatrix, distCoeffs)  
        frame = aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvecs, tvecs, 0.1)
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
    return frame, rvecs, tvecs

def makematrix(rvecs, tvecs):
    # build view matrix
    print(rvecs)
    rmtx = cv2.Rodrigues(rvecs[0][0])[0]
    print(rmtx,"---------------------------\n")
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
    main()
