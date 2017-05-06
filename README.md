# Massey-Omura
An implementation of the <b>Massey-Omura Cryptosystem</b>

This project was implemented in Python language using <b>gmpy2</b> library.</br>

There are 2 main entities, the client and the server, which we can call <b>Alice</b> and <b>Bob</b> respectively.</br>
<b>Alice</b> wants to send a message to <b>Bob</b> in a secure way but without the need to exchange any kind of keys.</br>
Infact, using this protocol there is no need of that. That's because the encryption and decryption functions are commutative.
Mathematical properties of congruences allows us to do that. 
