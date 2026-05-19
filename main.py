import streamlit as st
import math 
import random 

def generate_public_key(p, q):              
    # p and q are expected to be integers and primes (validated by caller)
    n = p * q                   # generate n value
    st.write("n = ", n)

    z = (p - 1) * (q - 1)         #generate z value
    st.write("z = ", z)

    e = generate_e(z, n)          #generate e value
    st.write("e = ", e)

    d = generate_d(e , z)        #generate d value
    st.write("d = ", d)

    st.write("Public key: (", n, ", ", e, ")")
    st.write("Private key: (", n, ", ", d, ")")

def generate_e(z, n):             #generate e value
    for e in range(2, z):
        if math.gcd(e, z) == 1:
            return e

def generate_d(e, z):
    for d in range(1, z * 5):
        if (e * d - 1) % z == 0 and d != e:
            return d


    def generate_public_key(p, q):              
        n = p * q                   #generate n value
        st.write("n = ", n)

        z = (p - 1) * (q - 1)         #generate z value
        st.write("z = ", z)

        e = generate_e(z, n)          #generate e value
        st.write("e = ", e)

        d = generate_d(e , z)        #generate d value
        st.write("d = ", d)

        st.write("Public key: (", n, ", ", e, ")")
        st.write("Private key: (", n, ", ", d, ")")

        return 0

    def generate_e(z):             #generate e value
        e = 65537  # very common RSA choice
        if math.gcd(e, z) == 1:
            return e

        # fallback if 65537 is not valid
        for e in range(3, z, 2):
            if math.gcd(e, z) == 1:
                return e

    def generate_d(e , z):             #generate d value
        d = 1 
        while True:
            if ((d * e) - 1) % z == 0:
                return d
            d += 1



#main function
st.title("Encryption and Decryption Using RSA Algorithm")


p = st.text_input("Enter a p prime value")

if p != "":
    p = int(p)

q = st.text_input("Enter a q prime value")

if q != "":
    q = int(q)

pressed = st.button("Generate")

if pressed == True:
    st.write("Generating public key...")
    generate_public_key(p, q)



