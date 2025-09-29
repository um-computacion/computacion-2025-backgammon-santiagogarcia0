# Changelog
Todas las notas importantes de cambios en este proyecto serán documentadas en este archivo.

## [0.3.0] - 2025-09-23
### Added
- CLI mejorada con:
  - Opción de mover fichas ingresando punto de origen y destino.
  - Visualización completa del tablero, bar y borneado.
  - Detección de condición de victoria cuando un jugador borneó todas sus fichas.
- Soporte en `Board` para:
  - Validación de movimientos con tiradas de dados.
  - Captura de fichas solitarias (hit).
  - Gestión de fichas en bar.
  - Borneado de fichas.
- `Game`: gestión de turnos con consumo de tiradas.
- `Dice`: soporte de tiradas dobles y validación con movimientos.
- Nuevas pruebas unitarias para:
  - Movimientos legales e ilegales.
  - Capturas (hit).
  - Bar y borneado.
  - Condición de fin de juego.

### Changed
- Refactorización y limpieza de código en `Board`, `Game` y `CLI`.
- Mejor legibilidad en impresión de tablero en la CLI.
- Aumento de cobertura de pruebas unitarias.

### Deprecated
-

### Removed
-

### Fixed
- Corrección de validaciones en movimientos que partían de puntos vacíos.
- Manejo consistente de turnos y tiradas consumidas.

### Security
-

## [0.2.0] - 2025-09-15
### Added
- CLI inicial con menú simple (tirar dados, mover fichas, mostrar tablero).
- Pruebas unitarias para `Board` y `Game`.
- Documentación actualizada en README.md.

### Changed
- Versión de proyecto actualizada de 0.1.0 a 0.2.0.

### Deprecated
-

### Removed
-

### Fixed
-

### Security
-

## [0.1.0] - 2025-09-01  
### Added
- Estructura inicial del proyecto.
- Archivos básicos: README.md, .gitignore, requirements.txt, CHANGELOG.md.