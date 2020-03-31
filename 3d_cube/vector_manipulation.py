import numpy as np
def normalVectorOfPlane(p1,p2,p3):
    '''
    return: Normal Vector of Plane. Might not be of unit length
    '''
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    return np.cross((p1-p2),(p3-p2)).tolist()

def perpendicularVectorFromPointToPlane(p1,p2,p3,p4):
    '''
    p1,p2,p3: points that define a plane
    p4: point not on plane
    return: shortest or pendicular vector from p4 to plane
    '''
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    p4 = np.array(p4)
    normalVector = np.array(normalVectorOfPlane(p1,p2,p3))
    D = np.dot(p1, normalVector)
    answer = p4 + (normalVector * ((D - np.dot(p4, normalVector))/np.linalg.norm(normalVector)**2))
    return answer.tolist()

def rectangleCentre(n1,n2,n3,n4,distance):
    n1 = np.array(n1)
    n2 = np.array(n2)
    n3 = np.array(n3)
    n4 = np.array(n4)
    distance = np.linalg.norm(distance)
    vector = np.cross([n3-n1], [n2-n4])
    centrePoint = 0.5 * (n3 + n1)
    normalVector = vector/(np.linalg.norm(n3-n1)*np.linalg.norm(n2-n4))
    vanishingPoint = centrePoint + normalVector * distance
    return vanishingPoint.tolist()[0]

def linePlaneIntersect(p1,p2,p3,p4,p5,epsilon):
    """
    :param p1: Point 1 of line
    :param p2: Point 2 of line
    :param p3: Point 1 of plane
    :param p4: Point 2 of plane
    :param p5: Point 3 of plane
    :param epsilon: margin of error
    :return: Point where line intersect plane
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    p4 = np.array(p4)
    p5 = np.array(p5)
    planeNormal = np.cross(p5-p3, p4-p3)
    planePoint = p3  # Any point on the plane
    lineDirection = p2-p1
    linePoint = p1  # Any point along the ray
    if abs(np.dot(lineDirection, planeNormal)) < epsilon:
        return None # line perpendicular to plane
    else:
        #L(s) = rayPoint + s(lineDirection), where s ia a constant
        s = np.dot(planeNormal, planePoint - linePoint)/np.dot(planeNormal, lineDirection)
        intersect = p1 + s*lineDirection
        return intersect.tolist()

def subv3v3(v1,v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    v3 = v1 - v2
    return v3.tolist()

def addv3v3(v1,v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    v3 = v1 + v2
    return v3.tolist()