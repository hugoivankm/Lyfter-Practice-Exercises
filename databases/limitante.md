## LIMITANTES: ##

- Valores de punto flotante solo pueden ser almacenados como `REAL`(8 Bytes IEEE punto flotante).
- `INTEGER` es almacenado hasta 8 bytes dependiendo de la magnitud del numero.
- `VARCHAR` no es un tipo valido en SQLLITE, se deben utilizar `TEXT` pero lo podemos limitar con `CHECK`
sin embargo length esta en terminos de bytes por `BLOB`, no caracteres
- `ENUM` no son directamente soportados pero podemos emularlos con `CHECK`
- FK en SQLite estan desabilitadas por default y necesitan habilitarlas con `PRAGMA foreign_keys = ON;`
- ALTER TABLE obliga a tomar una decision si poner un DEFAULT a datos existentes o permitir NULL,
se estan permitiendo NULLs por simplicidad, haciendo que el telefono sea opcional.
- Escapar comilla (') necesita dos comillas consecutivas ('')