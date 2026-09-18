# Copilot Instructions for Compilador C# a C++

## Project Overview

This is a C# to C++ compiler translator, currently in **Phase 1: Lexical Analysis**. The codebase is written entirely in Python and focuses on tokenizing C# source code, detecting lexical errors, and reporting token positions.

## Running the Code

### Graphical Interface

Launch the light-themed Tkinter interface from the repository root:

```bash
python3 src/interfaz.py
```

Use **Cargar archivo** to select a `.cs` file, then **Analizar** to run the existing
lexer. The interface displays the source code, token table, lexical errors, and totals.

### Import Path Setup

The entry points add the repository root to `sys.path`; internal modules use package imports from `src`.

## Architecture Overview

The lexical analyzer follows an **AFD (Finite State Automaton)** design split across specialized recognizer classes:

### Core Classes

| Module | Class | Responsibility |
|--------|-------|---|
| `tokens.py` | `Token`, `ErrorLexico`, `PALABRAS_RESERVADAS` | Data structures for tokens and lexical errors; reserved word set |
| `lector_archivo.py` | `LectorArchivo` | Character-by-character file reading; tracks position (line, column) |
| `manejador_errores.py` | `ManejadorErrores` | Collects and retrieves lexical errors |
| `reconocedor_tokens.py` | `ReconocedorTokens` | Main analyzer loop and dispatcher (`analizar()` method) |
| `reconocedor_ids.py` | `ReconocedorIDsYReservadas` | Identifies identifiers; distinguishes from reserved words |
| `reconocedor_numeros.py` | `ReconocedorNumeros` | Recognizes integers (`nint`) and floats (`nfloat`) |
| `reconocedor_cadenas.py` | `ReconocedorCadenasYCaracteres` | String and character literals |
| `reconocedor_simbolos.py` | `ReconocedorSimbolosYLimpieza` | Operators, delimiters, whitespace, and comment handling |

### Inheritance Pattern

All recognizers inherit from `ReconocedorTokens`, which provides access to:
- `self.lector` — File reader for character navigation
- `self.manejador_errores` — Error registry

Each child class implements a `procesar()` method that:
1. Records the starting position (line, column)
2. Accumulates lexema (token text)
3. Returns a `Token` or None

### Main Analyzer Loop (in `ReconocedorTokens.analizar()`)

1. **Skip whitespace** via `ReconocedorSimbolosYLimpieza.ignorar_espacios_y_saltos()`
2. **Dispatch by character type**:
   - `isalpha()` or `_` → Use `ReconocedorIDsYReservadas`
   - `isdigit()` → Use `ReconocedorNumeros`
   - `"` or `'` → Use `ReconocedorCadenasYCaracteres`
   - `/` with lookahead `//` or `/*` → Use `procesar_comentarios()`
   - Other → Use `ReconocedorSimbolosYLimpieza.procesar_operadores_y_delimitadores()`
3. Collect non-None tokens into the result list

## Key Code Conventions

### Position Tracking

- **Characters** are tracked one at a time using `LectorArchivo.siguiente_caracter()`
- **Line breaks** (`\n`) reset `columna` to 1 and increment `renglon`
- Always capture position **before** processing: `renglon, columna = self.lector.renglon, self.lector.columna`

### Lookahead Pattern

```python
if c == '/' and self.lector.espiar() in ('/', '*'):
    # Process comment
```
Use `lector.espiar(offset=1)` for single character lookahead; `offset` defaults to 1.

### Reserved Words

Check membership in `PALABRAS_RESERVADAS` (a set in `tokens.py`) to distinguish keywords from regular identifiers. Update `PALABRAS_RESERVADAS` when adding new keywords.

### Error Reporting

- Unclosed multiline comments `/* ... (EOF)` are logged via `manejador_errores.registrar_error()`
- Invalid characters generate `ErrorLexico` objects with exact line/column
- Use `manejador_errores.obtener_errores()` to retrieve all errors after analysis

### Circular Import Workaround

`ReconocedorTokens.analizar()` uses **delayed imports** to avoid circular dependencies:
```python
from reconocedor_ids import ReconocedorIDsYReservadas
# (imported inside method, not at module level)
```
Follow this pattern when adding new recognizers.

## Recognized Tokens

| Category | Pattern | Token Type | Example |
|----------|---------|-----------|---------|
| **Identifiers** | `[a-zA-Z_][a-zA-Z0-9_]*` | `id` | `miVariable` |
| **Integers** | `[0-9]+` | `nint` | `42` |
| **Floats** | `[0-9]+\.[0-9]+` | `nfloat` | `3.14` |
| **Strings** | `"..."` | `LiteralCadena` | `"Hello"` |
| **Characters** | `'.'` | `LiteralCaracter` | `'a'` |
| **Reserved** | (set in `PALABRAS_RESERVADAS`) | Various | `class`, `void`, `if` |
| **Operators** | `=`, `==`, `+`, `+=`, `++`, `-`, `-=`, `--`, `*`, `/`, `<`, `<=`, `>`, `>=`, `!=` | Literal type | `+` → `'+'` |
| **Delimiters** | `{`, `}`, `(`, `)`, `[`, `]`, `;`, `,`, `.`, `$` | Literal type | `{` → `'{'` |
| **Comments** | `//` (line) or `/* */` (block) | (filtered out) | Ignored |

## Testing & Validation

- No automated test framework is set up yet (Phase 1 only)
- Manual validation: Run with `HolaMundo.cs` and visually inspect token output for correctness
- To debug: Add `print()` statements in recognizer methods; check line/column tracking in `LectorArchivo.actualizar_posicion()`

## Future Phases

- **Phase 2**: Syntactic analysis (parser)
- **Phase 3**: Symbol table
- **Phase 4**: C++ code generation

These phases will build on the token stream produced by Phase 1.
