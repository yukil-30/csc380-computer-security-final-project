import streamlit as st
import pandas as pd
from utils import generate_keys, is_prime

def reset_encryption():
    st.session_state.ciphertext = None
    st.session_state.steps = None
    st.session_state.decrypted = None
    st.session_state.decrypt_steps = None

def reset_decryption():
    st.session_state.decrypted = None
    st.session_state.decrypt_steps = None

st.set_page_config(layout="centered")

st.title("Group E: RSA Encryption Demo")
st.divider()

# SESSION STATE
if "key_pair" not in st.session_state:
    st.session_state.key_pair = None

if "ciphertext" not in st.session_state:
    st.session_state.ciphertext = None

if "steps" not in st.session_state:
    st.session_state.steps = None

if "decrypted" not in st.session_state:
    st.session_state.decrypted = None

if "decrypt_steps" not in st.session_state:
    st.session_state.decrypt_steps = None

with st.expander("Generate Key 🔑", expanded=True):
    st.write("### Step 1: Enter prime numbers")

    p_input = st.text_input("Enter a p prime value")
    q_input = st.text_input("Enter a q prime value")

    # Validate inputs safely
    p, q = None, None

    if p_input:
        try:
            p = int(p_input)
        except ValueError:
            st.error("p must be an integer")

    if q_input:
        try:
            q = int(q_input)
        except ValueError:
            st.error("q must be an integer")

    st.write("### Step 2: Generate keys")

    pressed = st.button("Generate")

    if pressed:

        if p is None or q is None:
            st.warning("Please enter valid integers for p and q")
            st.stop()

        elif not is_prime(p) or not is_prime(q):
            st.warning("Please enter valid prime numbers")
            st.stop()
        else:
            st.write("Generating public key...")
            keypair, n, z = generate_keys(p, q)
            e, _ = keypair.public
            d, _ = keypair.private
            st.session_state.key_pair = keypair

            # Clear dependent data
            st.session_state.ciphertext = None
            st.session_state.steps = None
            st.session_state.decrypted = None
            st.session_state.decrypt_steps = None
            st.success("Keys generated successfully!")

        st.write("### Computed Values")

        with st.expander(f"n = {n}", expanded=True):
            st.latex(r"n = p \times q")
            st.latex(fr"n = {p} \times {q} = {n}")

        with st.expander(f"z = {z}", expanded=True):
            st.latex(r"z = (p - 1)(q - 1)")
            st.latex(fr"z = ({p}-1)({q}-1) = {z}")

        with st.expander(f"e = {e}", expanded=True):
            st.latex(r"e = 65537")
            st.latex(fr"\gcd(e, z) = \gcd(65537, {z}) = 1")

        with st.expander(f"d = {d}", expanded=True):
            st.latex(r"d \equiv e^{-1} \mod z")
            st.latex(fr"d \equiv {e}^{{-1}} \mod {z}")
            st.latex(fr"d = {d}")


if st.session_state.key_pair is not None:
    e, n = st.session_state.key_pair.public
    d, _ = st.session_state.key_pair.private

    st.write("### Keys")
    st.code(f"Public Key:  ({e}, {n})")
    st.code(f"Private Key: ({d}, {n})")

st.divider()
st.write("## 💬 Encryption / Decryption")

col1, col2 = st.columns(2)

with col1:
    st.write("### 🔐 Encrypt")

    if st.session_state.key_pair is None:
        st.warning("Generate keys first")
    else:
        message = st.text_area("Enter message to encrypt", key="enc_msg", on_change=reset_encryption)

        e, n = st.session_state.key_pair.public

        if message:
            if any(ord(c) >= n for c in message):
                st.error("Character value exceeds n")
                st.stop()

        if st.button("Encrypt", key="encrypt_btn"):
            ciphertext, steps = st.session_state.key_pair.encrypt(message)

            st.session_state.ciphertext = ciphertext
            st.session_state.steps = steps

        # Show results
        if st.session_state.get("ciphertext"):
            st.write("#### Ciphertext")
            st.code(st.session_state.ciphertext)

        if st.session_state.get("steps"):
            st.write("#### Encryption Table")
            st.table(pd.DataFrame(st.session_state.steps))

import json

with col2:
    st.write("### 🔓 Decrypt")

    if st.session_state.key_pair is None:
        st.warning("Generate keys first")
    else:
        cipher_input = st.text_area(
            "Paste ciphertext (JSON list)",
            placeholder="[123, 456, 789]",
            key="dec_input",
            on_change=reset_decryption
        )

        parsed_cipher = None

        if cipher_input:
            try:
                parsed_cipher = json.loads(cipher_input)
                if not isinstance(parsed_cipher, list):
                    st.error("Ciphertext must be a list of integers")
                    parsed_cipher = None
            except:
                st.error("Invalid JSON format")

        if st.button("Decrypt", key="decrypt_btn"):
            if parsed_cipher is None:
                st.warning("Enter valid ciphertext")
            else:
                plaintext, steps = st.session_state.key_pair.decrypt(parsed_cipher)

                st.session_state.decrypted = plaintext
                st.session_state.decrypt_steps = steps

        if st.session_state.get("decrypted"):
            st.write("#### Plaintext")
            st.success(st.session_state.decrypted)

        # Show results
        if st.session_state.get("decrypt_steps"):
            st.write("#### Decryption Table")
            st.table(pd.DataFrame(st.session_state.decrypt_steps))
