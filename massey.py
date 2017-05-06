import gmpy2

# a big prime number
PRIME = 4294967291
state = gmpy2.random_state()

# split a string in chunks of specified length
def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def generate_keys(prime = PRIME):
	while True:
		e = gmpy2.mpz_random(state, prime-2)
		if gmpy2.gcd(e, prime-1) == 1 and e > 2:
			break
	d = gmpy2.invert(e, prime-1)

    # return encryption and decryption keys
	return e,d


# used also for decryption
def crypt_chunk(chunk, key, prime = PRIME):
    # convert the chunk in a number
	num = 0
	for c in chunk:
		num *= 256
		num += ord(c)

	result = gmpy2.powmod(num, key, prime)
	vect = []
	for i in range(0, len(chunk)):
		vect.append(chr(result%256))
		result = result / 256

	return "".join(reversed(vect))
