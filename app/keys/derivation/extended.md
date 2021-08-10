# Generación de llaves extendidas (BIP-32)

Las llaves extendidas son una *llave privada* y una *llave pública* que permiten derivar nuevas llaves para una cartera jerárquica determinista.

Se conoce como llave extendida, porque al momento de generar una *llave privada* se le asocia directamente un *código de cadena*, *chain code* en inglés.

A partir de una **semilla** se generar una **llave privada maestra** junto con el **código de cadena** asociado, aplicando el algoritmo de hashing HMAC-SHA512 

![Llave privada extendida](/media/extended_keys.jpg?raw=true)

