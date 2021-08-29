# Conceptos Básicos de Criptografía

Existen dos tipos de cifrados con base en el método para descifrar el mensaje: simétrico y asimétrico.


## Criptografía de Curva Elíptica (ECDSA)

ecdsa

## Codificación Base58Check

Base58Check Base58Check version prefix and encoded result examples

| Tipo                           | Version (hex) | Base58 Resultado |
|--------------------------------|---------------|------------------|
| Dirección Bitcoin              | 0x00          | 1                |
| Dirección P2SH                 | 0x05          | 3                |
| Dirección SegWit P2SH-P2WPKH   | 0x05          | 3                |
| Dirección Testnet Bitcoin      | 0x6F          | m \| n           |
| Llave Privada WIF              | 0x80          | 5 \| K \| L      |
| BIP38 Llave Privada Encriptada | 0x0142        | 6P               |
| BIP32 Llave Pública Extendida  | 0x0488B21E    | xpub             |

