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

La administración de nuestros fondos sería muy sencilla, si de la misma manera que reutilizamos nuestro correo electrónico, utilizáramos una y otra vez la misma dirección para recibir y transferir fondos. Pues así, únicamente tendríamos que preocuparnos de mantener segura una sola llave privada.

Sin embargo, este modelo no es muy recomendable por la siguiente razón. Como ya vimos, una dirección **(A)** de Bitcoin está protegida por 2 capas de encriptación, por tanto, si un adversario quisiera robar los fondos de una dirección, primero tendría que romper la encriptación provista por el algoritmo `HASH160` para obtener la llave pública y posteriormente tendría que romper la encriptación de `ECDSA` para obtener la llave privada.

Al momento de generar una transacción, para gastar los fondos presentes en una dirección, como lo solicita el [Pay-to-Public-Key-Hash (P2PKH)](), es necesario revelar a la red pública que el usuario es dueño de la llave pública que apunta a dicha dirección. Si, en lugar de generar una nueva dirección, reutilizamos aquella de la cual hemos revelado la llave pública, un adversario tendría que romper sólo la encriptación del algoritmo `ECDSA` para robar los fondos. A la fecha, esto sigue siendo computacionalmente imposible.

Además de esta vulnerabilidad, la privacidad del dueño de la dirección podría verse comprometida pues todos los fondos que se muevan podrán ser fácilmente triangulados mediante un análisis de la información en la Blockchain. 

Por esta razón, es una buena práctica generar una nueva, y fresca ❄️, dirección de Bitcoin cada vez que se vayan a recibir fondos.

<p align="center">
    <img src="/media/wallet_simple.jpg?raw=true" width="600">
</p>

deterministica:

<p align="center">
    <img src="/media/wallet_deterministic.jpg?raw=true" width="600">
</p>

En inglés se conocen como *Hierarchical Deterministic wallets*, o simplemente HD wallets.

<p align="center">
    <img src="/media/wallet_hd.jpg?raw=true" width="600">
</p>