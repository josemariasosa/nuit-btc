# Generación de palabras mnemónicas (BIP-39)

La secuencia de palabras mnemónicas, o **semilla mnemónica**, es la representación codificada de un número aleatorio grandísimo. A partir de esta secuencia de palabras se crea una **semilla**, que puede ser utilizada para recrear, de manera segura y estándar, todas las direcciones y llaves extendidas de una cartera jerárquica determinista.

Por lo general, una **semilla** se representa utilizando un número hexadecial. Un ejemplo se muestra a continuación, comienza con `0x` para indicar que está codificado en hexadecimal. La semilla es de **64 bytes**.

```py
0x1e64005ec6246b473c7af8f59b39f1a98b493ac02a2757c7902a4f2265e4d6cb2697d1858d35cda6a404e3c1d4d46733aa8129d2c4c9b2d917faba88a77df488
```

Imaginemos tener que escribir en una hoja de papel dicho número para respaldar nuestra cartera. Estaríamos propensos fácilmente errores. Es por eso que se definió un estándar, conocido como [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), para codificar de una manera fácil de leer y almacenar, la semilla.

La representación codificada con BIP-39 de la **semilla** anterior es:

```text
sample tooth steak column crime rib woman budget job inch throw dog
```

Mucho más sencillo de manejar y almacenar 😺.

Los tres pasos para generar una secuencia de palabras mnemónicas son:

1. [Generar Entropía](https://github.com/josemariasosa/nuit-btc/blob/master/docs/mnemonic.md#1-generar-entrop%C3%ADa)
2. [De Entropía a palabras Mnemónicas](https://github.com/josemariasosa/nuit-btc/blob/master/docs/mnemonic.md#2-de-entrop%C3%ADa-a-palabras-mnem%C3%B3nicas)
3. [De palabras Mnemónicas a Semilla](https://github.com/josemariasosa/nuit-btc/blob/master/docs/mnemonic.md#3-de-palabras-mnem%C3%B3nicas-a-semilla)


## 1. Generar Entropía

La [**entropía**](https://es.wikipedia.org/wiki/Entrop%C3%ADa) es un concepto complejo y hasta contradictorio, dependiendo de su interpretación. Si tomamos la definición propuesta por el físico austríaco [Ludwig Boltzmann](https://es.wikipedia.org/wiki/Ludwig_Boltzmann) entre 1890 y 1900, la entropía es un parámetro, una medida, para el desorden. Es la probabilidad de un estado particular.

Una manera de imaginarlo es dejando caer un vaso de cristal al suelo. Tenderá a romperse y a esparcirse, mientras que jamás será posible que, lanzando trozos de cristal, se construya un vaso por sí solo.

Llevando este concepto al contexto de Bitcoin, es necesario generar entropía para que, de la misma manera que con las piezas del vaso, sea imposible que alguien más pueda regenerar aleatoriamente nuestra llave privada.

Para una computadora/máquina, es prácticamente imposible generar entropía pura, pues está ligada a procesos deterministicos que permiten únicamente la generación de [números pseudoaleatorios](https://es.wikipedia.org/wiki/N%C3%BAmero_pseudoaleatorio). Es por eso que para generar un número completamente aleatorio, que jamás haya sido creado, ni visto, anteriormente, la cartera [Nuit-BTC](https://github.com/josemariasosa/nuit-btc) le permite al usuario generar entropía mediante el lanzamiento de un dado `n` veces.

Lanzar un dado físico, y justo, en **al menos 99 ocasiones**, permitirá capturar la suficiente entropía para construír una llave privada segura.

Los siguientes pasos se llevan a cabo para generar entropía:


### I. Tirar un dado 🎲

Lanzar un dado al menos 99 veces y capturar los lanzamientos en un `string`.

```py
r = '51646134561234651234651543212234615341562346512364156234651234651234651234615234561235461513645123645'
```

Para el ejemplo se tiró el dado 101 veces.


### II. Seleccionar un número de palabras Mnemónicas 📝

Definir un número de palabras mnemónicas dentro del siguiente `set`: `{12, 15, 18, 21, 24}`.

Este número se selecciona a partir de la conveniencia y el caso de uso particular de cada persona. Es más sencillo memorizar un menor número de palabras, sin embargo se recomiendan utilizar 24 palabras, para una mayor seguridad.


### III. Calcular Hash #️⃣

Revisando la [**Tabla I de conversión de entropía**](https://github.com/josemariasosa/nuit-btc/blob/master/docs/mnemonic.md#tabla-i-conversi%C3%B3n-de-entrop%C3%ADa-en-bits), podemos observar la cantidad de bits `ENT`necesarios, en función del número de palabras mnemónicas, para convertir nuestro `string` de lanzamientos `r` en bits de entropía.

Para 24 palabras mnemónicas, se necesitan 256 bits de entropía, por lo tanto, utilizamos el algoritmo [SHA256](https://docs.python.org/3/library/hashlib.html#hash-algorithms).

```py
import hashlib

br = r.encode()                             # Convertir str a bytes
h = hashlib.sha256(br).digest()             # Obtener el digest del hash en bytes
```

Para un menor número de palabras mnemónicas utilizamos el algoritmo [SHAKE](https://docs.python.org/3/library/hashlib.html#shake-variable-length-digests) que permite generar un hash de longitud variable.

```py
import hashlib

br = r.encode()                             # Convertir str a bytes
h = hashlib.shake_256(br).digest(128 // 8)  # Obtener el digest del hash en bytes
```


### IV. Convertir Hash a número binario 0️⃣1️⃣

```py
i = int.from_bytes(h, 'big')                # Convertir bytes a entero big-endian
b = bin(i)[2:]                              # Convertir entero a bits | Retirar prefijo `0b`
entropy = b.zfill(len(h) * 8)               # Incluir zeros a la izquierda
```

Al final, la entropía para nuestro ejemplo `r`, utilizando 24 palabras resultaría en:

```py
print(entropy)
# 0110111111100110000010010101011110110100000000001001100100011111111101000010011101000010001011010100011110110000101101001010011110100001101100000101101110110000000011100011101101101101001010111011110001111000101011010101110101100101010110010010100110101111
```


## 2. De Entropía a palabras Mnemónicas

La entropía está dada por un número binario aleatorio `eg. 10101001` de longitud: `128, 160, 192, 224 o 256` bits. A partir de este número, se calcula el *checksum*, que nos ayuda a detectar y prevenir errores en la secuencia de palabras.

El tamaño del *checksum* está en función de la longitud de la entropía.

```text
CS = longitud_checksum
ENT = longitud_entropía

CS = ENT / 32
```

El número de palabras mnemónicas se determina sumando la longitud de la entropía y del *checksum*.

```text
MS = número_de_palabras_mnemónicas

MS = (ENT + CS) / 11
```

Un resumen de los cálculos de estos valores se muestra en la **Tabla I**.


##### Tabla I. Conversión de entropía (en bits)

|  ENT  | CS | ENT+CS |  MS  |
|-------|----|--------|------|
|  128  |  4 |   132  |  12  |
|  160  |  5 |   165  |  15  |
|  192  |  6 |   198  |  18  |
|  224  |  7 |   231  |  21  |
|  256  |  8 |   264  |  24  |


Los siguientes pasos se llevan a cabo para generar las palabras mnemónicas a partir de la entropía:

![De entropía a palabras mnemónicas](/media/entropy_to_mnemonic.jpg?raw=true)


### I. Calcular el checksum ✅

El *checksum*, en Python 🐍, se calcula convirtiendo la entropía en un `bytearray`, luego calculando el hash utilzando el algoritmo SHA256.

El hash resultante se convierte a número binario y se seleccionan los `CS` primeros valores.

```python
def bits_to_bytearray(entropy: str) -> bytearray:
    h = hex(int(entropy, 2))[2:]
    if len(h) % 2 != 0:
        h = '0' + h
    return bytearray.fromhex(h)

def generate_checksum(entropy: str) -> str:
    """Entropy is in Binary but must be converted into bytearray."""
    b = bits_to_bytearray(entropy)
    h = hashlib.sha256(b).digest()
    checksum_length = len(entropy) // 32
    checksum_bits = bin(int.from_bytes(h, 'big'))[2:].zfill(256)
    checksum = checksum_bits[:checksum_length]
    return str(checksum)
```


### II. Concatenar la entropía + checksum 🖇

La entropía secreta se concatena con el checksum para permitir formar una cadena binaria con `11 bits` por cada palabra mnemónica.

Posteriormente, dicha cadena se separa en *chunks* de 11 bits.

```python
entropy = '0110111111100110000010010101011110110100000000001001100100011111111101000010011101000010001011010100011110110000101101001010011110100001101100000101101110110000000011100011101101101101001010111011110001111000101011010101110101100101010110010010100110101111'
checksum = generate_checksum(entropy)

full = entropy + checksum
```


### III. Mapear chunks con palabras Mnemónicas 🗺

Cada uno de los chunks de `11 bits` puede ser individualmente mapeado con la lista de palabras estándar definida en el BIP-39. La lista completa de palabras se encuentra en múltiples idiomas, incluyendo inglés, español, francés e italiano. La lista completa de palabras puede ser revisada en el [BIP-39 Wordlist](https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md).

```python
wordlist = import_words_for_language()              # From BIP-39

def to_mnemonic(full: str) -> str:
    result = []
    for i in range(len(full) // 11):
        idx = int(full[i * 11 : (i + 1) * 11], 2)
        result.append(wordlist[idx])
    result = ' '.join(result)
    return result
```


## 3. De palabras Mnemónicas a Semilla

Para poder generar una semilla a partir de las `12, 15, 18, 21 o 24` palabras, primero se valida que el *checksum* sea correcto y posteriormente se pasa a través de una función PBKDF2, Password-Based Key Derivation Function 2. Utilizando los siguientes parámetros:

- **2048** rondas de HMAC-SHA512.
- Password: secuencia de palábras mnemónicas.
- Salt: "mnemonic" + *passphrase* (la palabra "mnemonic" es un string fijo que se añade).
- El Password y la Salt están codificados como UTF-8 NFKD.

![Palabras mnemónicas a semilla](/media/mnemonic_seed.jpg?raw=true)

El resultado es una semilla de 512 bits, o 128 caracteres en hexadecimal.



<!-- 
**¿Qué tan grande podría llegar a ser una llave privada?**

El número aleatorio podría ir tan alto como `2^256`, o lo que es aproximadamente lo mismo un 1 seguido de 77 ceros: `10^77`. Podríamos pensarlo de la siguiente manera: existen tantas posibles llaves privadas en Bitcoin como el número de átomos en un billón de galaxias. -->


## 