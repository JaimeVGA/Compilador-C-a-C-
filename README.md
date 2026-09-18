# Compilador C# a C++

Compilador que lee codigo fuente en **C#** y lo traduce a **C++**. El proyecto se desarrolla por fases; actualmente se encuentra en la primera: el **analizador lexico**.

---

## Fases del compilador

- [x] Fase 1 — Analisis lexico
- [ ] Fase 2 — Analisis sintactico (parser)
- [ ] Fase 3 — Tabla de simbolos
- [ ] Fase 4 — Generacion de codigo C++

---

## Estructura del repositorio

```
Compilador-C-a-C-/
├── src/
│   ├── modelos/
│   │   └── tokens.py                  # Token, ErrorLexico, PALABRAS_RESERVADAS
│   ├── persistencia/
│   │   ├── lector_archivo.py          # LectorArchivo
│   │   ├── reconocedor_tokens.py      # ReconocedorTokens (clase base)
│   │   ├── reconocedor_ids.py         # ReconocedorIDsYReservadas
│   │   ├── reconocedor_numeros.py     # ReconocedorNumeros
│   │   ├── reconocedor_cadenas.py     # ReconocedorCadenasYCaracteres
│   │   ├── reconocedor_simbolos.py    # ReconocedorSimbolosYLimpieza
│   │   └── manejador_errores.py       # ManejadorErrores
│   ├── presentacion/
│   │   ├── ventana_resultados.py
│   │   ├── tabla_base.py
│   │   ├── tabla_errores.py
│   │   ├── tabla_simbolos.py
│   │   ├── tira_tokens.py
│   │   └── estilos.py
│   └── interfaz.py                    # Punto de entrada de la interfaz gráfica
├── automatas Jflap/                   # Diagramas AFD en formato JFlap
├── documentacion/                     # Documentacion del proyecto
└── README.md
```

---

## Fase 1 — Analizador Lexico

El analizador lexico es la primera etapa del compilador. Se encarga de:

1. **Leer** el archivo fuente caracter por caracter
2. **Limpiar** espacios en blanco y comentarios (`//` y `/* */`)
3. **Tokenizar** agrupando caracteres en tokens validos segun el AFD
4. **Detectar errores** lexicos reportando el caracter, renglon y columna exacta

### Arquitectura (basada en UML)

Los modulos siguen el diagrama de clases definido en la documentacion:

| Modulo | Clase | Responsabilidad |
|--------|-------|-----------------|
| `tokens.py` | `Token`, `ErrorLexico` | Estructuras de datos del analizador |
| `lector_archivo.py` | `LectorArchivo` | Lectura y navegacion del archivo fuente |
| `manejador_errores.py` | `ManejadorErrores` | Registro y consulta de errores lexicos |
| `reconocedor_tokens.py` | `ReconocedorTokens` | Clase base y ciclo principal `analizar()` |
| `reconocedor_ids.py` | `ReconocedorIDsYReservadas` | Identificadores y palabras reservadas |
| `reconocedor_numeros.py` | `ReconocedorNumeros` | Enteros (`nint`) y flotantes (`nfloat`) |
| `reconocedor_cadenas.py` | `ReconocedorCadenasYCaracteres` | Literales de cadena y caracter |
| `reconocedor_simbolos.py` | `ReconocedorSimbolosYLimpieza` | Operadores, delimitadores y comentarios |

### Tokens reconocidos

**Identificadores y literales**

| Patron | Token | Ejemplo |
|--------|-------|---------|
| `letra(letra\|digito\|_)*` | `id` | `miVariable` |
| `digito+` | `nint` | `42` |
| `digito+.digito+` | `nfloat` | `3.14` |
| `"..."` | `LiteralCadena` | `"Hola Mundo"` |
| `'.'` | `LiteralCaracter` | `'a'` |

**Palabras reservadas**

`using` `namespace` `class` `static` `void` `int` `float` `double` `string` `bool` `if` `else` `for` `while` `return` `Console` `Write` `Line` `Read` `Parse`

**Operadores**

`=` `==` `+` `+=` `++` `-` `-=` `--` `*` `/` `<` `<=` `>` `>=` `!=` `->`

**Delimitadores**

`{` `}` `(` `)` `[` `]` `;` `,` `.` `$`

### Como ejecutar

#### Interfaz grafica

Desde la raiz del repositorio:

```bash
python3 src/interfaz.py
```

La interfaz permite cargar un archivo `.cs`, ejecutar el analisis lexico y consultar
los tokens y errores encontrados.




**Materia:** Compiladores — 5to Semestre
**Universidad:** UTM
