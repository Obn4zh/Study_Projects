import java.math.BigInteger
import java.security.SecureRandom
import java.nio.charset.Charset


class RSA (private val bitLength: Int) {
    private var publicKey: BigInteger
    private var privateKey: BigInteger
    private var modulus: BigInteger

    init {
        val random = SecureRandom()
        val p = BigInteger.probablePrime(bitLength / 2, random)
        val q = BigInteger.probablePrime(bitLength / 2, random)
        val phi = (p.subtract(BigInteger.ONE)).multiply(q.subtract(BigInteger.ONE))
        modulus = p.multiply(q)
        publicKey = BigInteger.probablePrime(bitLength / 2, random)
        privateKey = publicKey.modInverse(phi)
    }

    fun encrypt(message: String): BigInteger {
        val m = BigInteger(message.toByteArray(Charset.forName("UTF-8")))
        return m.modPow(publicKey, modulus)
    }

    fun decrypt(ciphertext: BigInteger): String {
        val m = ciphertext.modPow(privateKey, modulus)
        return String(m.toByteArray(), Charset.forName("UTF-8"))
    }

    // -*- coding: UTF-8 -*-

    fun pub_key(): BigInteger {
        return publicKey
    }

    fun priv_key(): BigInteger {
        return privateKey
    }
}

fun main() {
    val rsa = RSA(2048)
    val message = "Kak ispol`zovat russkiy?"
    val ciphertext = rsa.encrypt(message)
    val plaintext = rsa.decrypt(ciphertext)
    val pub = rsa.pub_key()
    val priv = rsa.priv_key()

    println("Original message: $message")
    println("Encrypted message: $ciphertext")
    println("Decrypted message: $plaintext")
    println("pub_key: $pub")
    println("priv_key: $priv")
}
