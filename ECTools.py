import numpy as np
import matplotlib.pyplot as plt

class Point():
    def __init__(self,x,y):
        """
        Initializes a new instance of Point class.

        Args:
            x (int): The value to assign to the x instance variable.
            y (int): The value to assign to the y instance variable.
        """
        self.x = x
        self.y = y

    def isInfinity(self):
        return False
    
    def isValid(self,group,curve):
        return True if self.isInfinity() else (self.y**2 % group.p) == ((self.x ** 3 + curve.a * self.x + curve.b) % group.p)

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y
    
    def __str__(self):
        return f"({self.x},{self.y})"

class PointAtInfinity(Point):
    def __init__(self):
        """
        Initializes a new instance of Point class for point at infinity.

        """
        self.x = None
        self.y = None

    def isInfinity(self):
        return True

    def __str__(self):
        return f"(Inf,Inf)"

class ECPoint():
    def __init__(self, point,group,curve, k = 1):
        """
        Initializes an instance of the class with a valid point, group, curve and optional k value.

        Args:
            point: A valid point.
            group: The group to which the point belongs.
            curve: The curve on which the point resides.
            k (optional): An integer representing the value of k. Defaults to 1.

        Raises:
            Exception: If the given point is invalid.

        Returns:
            None
        """        
        if not point.isValid(group,curve):
            raise Exception("Invalid point")
        self.point = point
        self.k = k

    def isInfinity(self):
        return (self.k == 0)
    
    def __eq__(self, __value: object) -> bool:
        return self.point == __value.point
    
    def __str__(self):
        return f"{self.point}.{self.k}"

class ECPointInfinity(ECPoint):
    def __init__(self):
        """
        Initializes a new instance of ECPoint class for point at infinity.

        """
        self.point = PointAtInfinity()
        self.k = 0

class ECCurve():
    def __init__(self,a,b):
        """
        Initialize a new instance of ECCurve with representation y^2 = x^3 + a*x + b with the given values.

        Args:
            a (any): The value to assign to `self.a`.
            b (any): The value to assign to `self.b`.
        """        
        self.a = a
        self.b = b

    def ec_add(self,P,Q,group):
        if P == ECPointInfinity():
            return Q
        elif Q == ECPointInfinity():
            return P
        
        if P.point.x == Q.point.x:
            if P.point.y != Q.point.y:
                return ECPointInfinity()
            elif P.point.y == 0:
                return ECPointInfinity()
            else:
                t = (3*P.point.x**2+self.a)*pow(2 * P.point.y,group.p-2,group.p) % group.p
        else:
            t = (Q.point.y - P.point.y) * pow(Q.point.x - P.point.x, group.p-2, group.p) % group.p

        x = (t**2 - P.point.x - Q.point.x) % group.p
        y = (t*(P.point.x - x) - P.point.y) % group.p
        return ECPoint(Point(x,y),group,self,P.k+Q.k)

    def ec_neg(self,P,group):
        return ECPoint(Point(P.point.x,-P.point.y % group.p),group,self,-P.k)

    def ec_sub(self,P,Q,group):
        return self.ec_add(P,self.ec_neg(Q,group),group)

    def __str__(self):
        if self.a == 0 and self.b != 0:
            return f"ECCurve : y^2 = x^3 + {self.b}"
        elif self.b == 0 and self.a != 0:
            return f"ECCurve : y^2 = x^3 + {self.a}"
        elif self.a == 0 and self.b == 0:
            return f"ECCurve : y^2 = x^3"
        else:
            return f"ECCurve : y^2 = x^3 + {self.a}x + {self.b}"
    
    def order(self,group,origin):
        return self.get_generated_points(group,origin)[1]

    def get_generated_points(self,group,origin):
        """
        Compute the list of points generated by repeatedly adding the given origin
        point to itself using the given group's elliptic curve addition operation.

        :param self: the current instance of the class
        :param group: the elliptic curve group to use for the operation
        :param origin: the starting point to generate more points from
        :return: a tuple containing the list of generated points and its length
        """        
        P = origin
        generatedPoints = list()
        generatedPoints.append(ECPointInfinity())
        while P not in generatedPoints and P != ECPointInfinity():
            generatedPoints.append(P)
            P = self.ec_add(P,origin,group)
        return generatedPoints,len(generatedPoints)

    def get_valid_points(self,group):
        """
        Computes the valid points on an elliptic curve defined by the parameters 'a', 'b'
        and the modulus 'p', given a group of points.

        :param self: A reference to the instance of the class containing the function.
        :param group: A group of points on the elliptic curve.
        :return: A list containing the valid points on the elliptic curve.

        The function starts by creating an empty list and appending the point at infinity.
        Then, for each x-coordinate in the range [0, p), it computes the corresponding y-coordinate
        using the elliptic curve equation. If the y-coordinate is zero, it adds the point (x,0) to the list.
        Otherwise, it searches for a modular square root of the y-coordinate modulo p by iterating over
        the range [1, p) and checking if y^2 is congruent to the y-coordinate modulo p. If a modular square root
        is found, it adds the points (x,y) and (x,p-y) to the list. Finally, it returns the list of valid points.
        """
        ret = list()
        ret.append(PointAtInfinity())
        for x in range(0,group.p):
            ysq = (x ** 3 + self.a * x + self.b) % group.p
            if ysq == 0:
                ret.append(Point(x,0))
            else:
                # Probably not the smartest way to get modular sqrt ... 
                for y in range(1, group.p):
                    if y*y % group.p == ysq:
                        ret.append(Point(x,y))
                        ret.append(Point(x,group.p-y))
                        break
        return ret



class ECGroup():
    def __init__(self, p):
        """
        Initializes a new instance of the class with the given prime number p.

        Raises:
        - Exception: if p is not prime. p must be prime as we use a shortcut for modular maths:
        pow(a, p-2, p).
        """
        self.p = p
        if not self.is_prime(p):
            raise Exception("p is not prime")       # p must be prime as we use some shortcut for modular maths : pow(a,p-2,p)

    def is_prime(self,n):
        if n < 2:
            return False
        if n == 2:
            return True
        for i in range(2,int(n**0.5)+1):
            if n % i == 0:
                return False
        return True

    def __str__(self):
        return f"ECGroup : prime = {self.p}"
    

class ECFactory(): 
    def __init__(self):
        pass

    def print_infos(self,group,curve):
        print(group)
        print(curve)

    def print_valid_points(self,group,curve):
        """
        Print and return the valid points on a given curve for a given group.

        :param group: the group of points to consider
        :param curve: the curve to search for valid points
        :return: a list of valid points on the curve for the group
        :rtype: list
        """
        pointList = curve.get_valid_points(group)
        print(f"{len(pointList)} valid points : ",end="")
        print(*pointList)
        return pointList

    def print_all_groups(self,group,curve):
        """
        Prints information about the given group and curve.
        Then, prints the valid points in the group.
        Finally, for each valid point, calculates the order and prints the origin,
        order, and generated sequence.

        Args:
            group: The group to print information about.
            curve: The curve to print information about.
        """        
        self.print_infos(group,curve)
        pointList = self.print_valid_points(group,curve)
        for item in pointList:
            origin = ECPoint(item,group,curve)
            result,order = curve.get_generated_points(group,origin)
            print("origin : "+str(item)+" / order : " + str(order)+ " / sequence : ",end="")
            print(*result)

    def print_group(self,group,curve,origin):
        """
        Prints out information about the given group and curve with respect to the specified origin.

        Args:
            group: The group to print information about.
            curve: The curve to print information about.
            origin: The origin to use for generating points.

        Returns:
            None

        Prints out the following information:
        - Information about the group and curve using self.print_infos().
        - Valid points for the group and curve using self.print_valid_points().
        - The generated points using curve.get_generated_points() with the specified group and origin.
        - The origin, order, and sequence of the generated points.
        """        
        self.print_infos(group,curve)
        self.print_valid_points(group,curve)
        org = ECPoint(origin,group,curve)
        result,order = curve.get_generated_points(group,org)
        print("origin : "+str(org)+" / order : " + str(order)+ " / sequence : ",end="")
        print(*result)

    def plot_group(self,group,curve,origin):
        
        org = ECPoint(origin,group,curve)
        result,order = curve.get_generated_points(group,org)

        xy = list()
        for item in result:
            if not item.isInfinity():
                xy.append([item.point.x,item.point.y,item.k])

        data = np.array(xy)
        x, y, k = data.T
        plt.scatter(x,y)           # If you just need points
        plt.xlabel("X")
        plt.ylabel("Y",rotation='horizontal')
        plt.title(str(curve)+" ["+str(group.p)+"] with origin "+str(origin)+" : order is "+str(order))

        # https://queirozf.com/entries/add-labels-and-text-to-matplotlib-plots-annotation-examples
        for x,y,k in zip(x,y,k):
            label = "1 Origin" if (k==1) else "{:d}".format(k)
            plt.annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center
            
            if (k != 1):
                n = 10*((x-ox)**2+(y-oy)**2)**0.5

                if len(xy) % 2 == 1:   # res = factory.print_group(ECGroup(11),ECCurve(0,7),Point(4,4))
                    if k < (len(xy)+1)//2:
                        color = 'b'
                    elif k > (len(xy)+1)//2 + 1:
                        color = 'g'
                    else:
                        color = 'r'
                else:
                    if k < (len(xy)+1)//2 + 1:    # res = factory.print_group(ECGroup(31),ECCurve(0,7),Point(25,16))
                        color = 'b'
                    elif k > (len(xy)+1)//2 + 1:
                        color = 'g'
                    else:
                        color = 'r'

                plt.arrow((x+ox)/2,(y+oy)/2,(x-ox)/n,(y-oy)/n, shape='full', lw=1, length_includes_head=True, head_width=0.1, color = color)
                plt.plot([ox, x],[oy, y], color = color)

            ox = x
            oy = y

        plt.grid()
        plt.show()
