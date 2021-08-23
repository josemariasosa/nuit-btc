# Generación de llaves extendidas (BIP-32)





Las llaves extendidas son una *llave privada* y una *llave pública* que permiten derivar nuevas llaves para una Cartera Jerárquica Determinista (HD Wallet).

Estas llaves facilitan la administración, resguardo y recuperación de los fondos, porque toda la informaición pública y privada se deriva a partir de una sola semilla. Podemos darnos cuenta de las ventajas, si comparamos una cartera deterministica contra sus dos alternativas:

- Reutilizar una misma llave pública para cada transacción.
- Generar un par de llaves pública y privada para cada transacción.






Se conoce como llave extendida, porque al momento de generar una *llave privada* se le asocia directamente un *código de cadena*, *chain code* en inglés.

A partir de una **semilla** se generar una **llave privada maestra** junto con el **código de cadena** asociado, aplicando el algoritmo de hashing HMAC-SHA512 

![Llave privada extendida](/media/extended_keys.jpg?raw=true)

