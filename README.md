# elliptic-curve-compute
 Basic elliptic curve calculation for experiment and learning.
 
 This simple python code will allow you to define an elliptic curve on the prime-field of your choice.
 It will allow you to display :
  - all the valid points (matching elliptic curve on the field)
  - use a valid origin point O to generate the sub-group of points using the scalar multiplication P=k.O (k varying from 0 to order of the sub-group)

 As an example, Bitcoin is using same method to generate the public key (with much bigger integer than this program can handle) :
  - O is the origin point : 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
  - Elliptic curve is y^2 = x^3 + 7 on the field 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
  - k is the scalar multiplicator (private key) : number that can be between 1 and 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 (order of generated sub-group)
  - P are the coordinates of the resulting point (and giving your public key) 
 
 The private/public address are derived from those datas. Security is mainly done by the fact that given a known public key (resulting P=k.O) you cannot guess the value of k (the private key).
 There are no other ways than brute force (trying as many k as needed and compare with P), and the size of number involved make impossible to check them all during a scan taking several zillions of universe age with all humanity computers working together (in fact this is in reality much longer than that ... but you get the idea).  


Here is an example of display for the curve y^2=x^3+7 over the field F17 (finite field with prime=17) :

![image](https://user-images.githubusercontent.com/26048157/233725032-49c5ea9d-4623-4d24-9502-a61db259d0c9.png)
