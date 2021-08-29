# Cartera Jerárquica Deterministica


## Direcciones, Llaves Públicas y Privadas

La manera más común de llevar a cabo transacciones en Bitcoin es a través del uso de direcciones. Una dirección de Bitcoin luce de la siguiente manera:

```text
1GCMeqbPtm4kWptMLJfj17WRoZSfL4qwFh
13UTodzv3xtNM7VUtKQD1sxwDq833XyjSa
1G2bAaF6Dtq3psAQHeg5qWgYKY3sKzrjBh
```

El `1` al inicio de la dirección, indica que se trata de una dirección de Bitcoin en la red principal, `mainnet`, y que fue generada a partir del hash de una llave pública. Esto quiere decir, que una dirección **(A)** la puede generar únicamente aquel que poseé la llave pública **(K)** que apunte a dicho hash. Y a su vez, una llave pública únicamente la puede generar aquel que conozca la respectiva llave privada **(k)**.

Todos los fondos transferidos a la dirección **(A)** únicamente podrán ser redimidos por quien controle la llave privada **(k)**.

El siguiente diagrama nos muestra cómo es posible pasar de una llave privada a una dirección de Bitcon, pero las operaciones criptográficas previenen que se pueda ir en sentido opuesto.

```
Llave privada    -- ECDSA -->    Llave pública    -- HASH160 -->    Dirección
     (k)                              (K)                              (A)
                 <---  X  ---                     <----  X  ----
```

El algoritmo [criptográfico de curva elíptica (ECDSA)](https://github.com/josemariasosa/nuit-btc/blob/master/docs/crypto.md#criptograf%C3%ADa-de-curva-el%C3%ADptica-ecdsa) permite generar una llave pública a partir de una llave privada, y además permite firmar digitalmente transacciones, comprobando que el firmante es poseedor del secreto.

Para generar una dirección se utiliza el algoritmo conocido comúnmente como `HASH160` el cual consta de una operación de doble de hash de una llave pública **(K)**, primero utilizando `SHA256` seguido de un `RIPEMD160`. Finalmente, para obtener una dirección con el formato correcto de una dirección de Bitcoin el hash se codifica mediante [Base58Check](https://github.com/josemariasosa/nuit-btc/blob/master/docs/crypto.md#codificaci%C3%B3n-base58check).


## Carteras de Bitcoin


En inglés se conocen como *Hierarchical Deterministic wallets*, o simplemente HD wallets.