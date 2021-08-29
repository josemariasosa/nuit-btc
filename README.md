# Nuit-BTC Wallet
🐈-₿

Implementación de una **Cartera Jerárquica Determinista** para Bitcoin (BTC).

La implementación será llevada a cabo en Python, y estará acompañada de una documentación extensa en Español, con el objetivo de que pueda servir como guía para  personas interesadas en aprender o desarrolar software propio.

El **objetivo** de esta implementación es principalmente didáctico. Cada operación será realizada utilizando únicamente la librería base de Python, sin módulos externos. Con el fin de que los interesados puedan comprender, con un gran nivel de detalle, cómo es que se genera cada bit, dentro de una cartera, de una llave y/o una transacción en Bitcoin. Eliminando la presencia de procesos oscuros, o de caja negra, transparentando así cada paso.

Para la implementación del algoritmo [criptográfico de curva elíptica (ECDSA)](https://github.com/josemariasosa/nuit-btc/blob/master/docs/crypto.md#criptograf%C3%ADa-de-curva-el%C3%ADptica-ecdsa) en Python se utilizó como referencia el libro de [**Programming Bitcoin**](https://github.com/jimmysong/programmingbitcoin) de Jimmy Song.


## Contenido

- [Cartera Jerárquica Deterministica](/docs/hdwallet.md)
- [Generación de palabras mnemónicas (BIP-39)](/docs/mnemonic.md)
- [Generación de llaves extendidas (BIP-32)](/docs/extended_key.md)


## Comienzo Rápido

### 1. Generación de semilla y palabras mnemónicas

Generar una semilla de manera aleatoria y rápida:

```python
from key.mnemonic import Mnemonic

m = Mnemonic(language="spanish", number_of_words=12)
secret = m.generate_user_keys()

print('mnemonic: ', secret.get('mnemonic'))
print('seed: ', secret.get('seed'))

# mnemonic:  echar perla turno tomar anillo viudo pizca envío grúa calma boa cien
# seed:  e83814fac124edf61aaed1f4e6c6c29a4ff774b82e096ab2bc2b086d7035eaee4c23a3a823b193515ba755159a4b60e5c7f0ad36b66a57ae13f8af8c6aebd7ad
```

Es posible, y muy recomendable, que la entropía sea provista por el usuario de manera manual, lanzando un dado al menos en 99 ocasiones. Esto se consigue utilizando el argumento `manually=True`.

```python
m = Mnemonic(language="spanish", number_of_words=12)
secret = m.generate_user_keys(manually=True)

print('mnemonic: ', secret.get('mnemonic'))
print('seed: ', secret.get('seed'))

#             -> Inserta el resultado del lanzamiento [1-6].
#             -> Únicamente valores entre 1 y 6 están permitidos.
#             -> Capturar al menos 99 lanzamientos.
#             -> Para terminar capture cualquier valor no permitido.

# Resultado del lanzamiento (1): 3
# Resultado del lanzamiento (2): 4
# Resultado del lanzamiento (3): 5
# Resultado del lanzamiento (4): 2
# Resultado del lanzamiento (5): 3
# Resultado del lanzamiento (6): 4
# Resultado del lanzamiento (7): 2
# Resultado del lanzamiento (8):
# WARNING: Input is only 18.095 bits of entropy

# mnemonic:  hoguera ofrecer tejado cohete goma trufa tapón humano engaño tira reunir cita
# seed:  5459e51dd1949ec27e0c70a4542001017b2122109ad50e1773db890c145689a99430fa9722e3726b1f1ca6aa37002e8849c24e25d6181c549c2cb2e8e213ad17
```


## La Nuit ⽉

<p align="center">
    <img src="/media/la_nuit.jpg?raw=true" height="600" width="600">
</p>

```
Porque la Nuit también quiere tener sus satoshis guardados de manera segura.
```
