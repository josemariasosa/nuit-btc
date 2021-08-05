# Generación de palabras mnemónicas

La secuencia de palabras mnemónicas, o **semilla mnemónica**, es la representación codificada de un número aleatorio enorme. A partir de esta secuencia de palabras se crea una **semilla**, que puede ser utilizada para recrear, de manera segura y estándar, todas las direcciones y llaves extendidas de una cartera jerárquica determinista.

Por lo general, una **semilla** se representa utilizando un número hexadecial. Un ejemplo se muestra a continuación, comienza con `0x` para indicar que está codificado en hexadecimal.

```py
0x1e64005ec6246b473c7af8f59b39f1a98b493ac02a2757c7902a4f2265e4d6cb2697d1858d35cda6a404e3c1d4d46733aa8129d2c4c9b2d917faba88a77df488
```

Imaginemos tener que escribir en una hoja de papel dicho número para respaldar nuestra cartera. Estaríamos propensos fácilmente errores. Es por esto que los desarrolladores de Bitcoin definieron un estándar, conocido como [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), para codificar de una manera amigable la semilla.

La representación codificada con BIP-39 de la **semilla** anterior es:

```text
sample tooth steak column crime rib woman budget job inch throw dog
```

Mucho más sencillo de manejar y almacenar.

Los tres pasos para generar una secuencia de palabras mnemónicas son:

1. [Generar Entropía]()
2. [De Entropía a palabras Mnemónicas]()
3. [De palabras Mnemónicas a Semilla]()


## 1. Generar Entropía


## 2. De Entropía a palabras Mnemónicas

![De entropía a palabras mnemónicas](/media/entropy_to_mnemonic.jpg?raw=true)

La entropía es un número binario aleatorio `eg. 10101001` de longitud `128, 160, 192, 224 o 256` bits. A partir de este número, se calcula un *checksum* que nos ayuda a detectar errores en la secuencia de palabras mnemónicas.

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

Un resumen de los valores permitidos se muestra en la siguiente tabla.

|  ENT  | CS | ENT+CS |  MS  |
|-------|----|--------|------|
|  128  |  4 |   132  |  12  |
|  160  |  5 |   165  |  15  |
|  192  |  6 |   198  |  18  |
|  224  |  7 |   231  |  21  |
|  256  |  8 |   264  |  24  |

Como buena práctica, por seguirdad se recomienda utilizar una entropía de 256 bits, lo que resultaría en una secuencia de palábras mnemónicas de 24.

Por último, cada palabra mnemónica está directamente mapeada utilizando 11 bits. 

## 3. De palabras Mnemónicas a Semilla




<!-- 
**¿Qué tan grande podría llegar a ser una llave privada?**

El número aleatorio podría ir tan alto como `2^256`, o lo que es aproximadamente lo mismo un 1 seguido de 77 ceros: `10^77`. Podríamos pensarlo de la siguiente manera: existen tantas posibles llaves privadas en Bitcoin como el número de átomos en un billón de galaxias. -->


## 