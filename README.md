# Nuit-BTC Wallet
🐈-₿

Implementación de una **Cartera Jerárquica Determinista** para Bitcoin (BTC).

La implementación será llevada a cabo en Python, y estará acompañada de una documentación extensa en Español, con el objetivo de que pueda servir como guía para  personas interesadas en aprender o desarrolar software propio.

El **objetivo** de esta implementación es principalmente didáctico. Cada operación será realizada utilizando únicamente la librería base de Python, sin módulos externos. Con el fin de que los interesados puedan comprender, con un gran nivel de detalle, cómo es que se genera cada bit, dentro de una cartera, de una llave y/o una transacción en Bitcoin. Eliminando la presencia de procesos oscuros, o de caja negra, transparentando así cada paso.

Para la implementación del algoritmo criptográfico de curva elíptica (ECDSA) en Python se utilizó como referencia el libro de [**Programming Bitcoin**](https://github.com/jimmysong/programmingbitcoin) de Jimmy Song.


## Contenido

- [Cartera Jerárquica Deterministica](/docs/hdwallet.md)
- [Generación de palabras mnemónicas (BIP-39)](/docs/mnemonic.md)
- [Generación de llaves extendidas (BIP-32)](/docs/extended_key.md)

![La Nuit](/media/la_nuit.jpg?raw=true)

```
Porque la Nuit también quiere tener sus bitcoins guardados de manera segura.
```
