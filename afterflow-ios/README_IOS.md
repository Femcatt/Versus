# Afterflow para iOS — port no oficial

Base: Afterflow 2.1.6 de prsevend, commit
`8b12bcb4ce1ca9c9c01e6d437a5f0d05f35a421e`.
Código original: https://github.com/afterflow-gd/afterflow/tree/2.1.6
Licencia MIT original conservada en LICENSE.

## Objetivo y controles

Este proyecto adapta el código fuente a iPhone ARM64 con Geometry Dash
**2.2081** y Geode **5.11.2**. La versión del port es `2.1.6-ios.1`.
Una compilación correcta aún requiere pruebas en un iPhone para confirmar
que la predicción, los toques y los cambios de modo funcionan correctamente.
No se declara compatibilidad comprobada con otras versiones de GD.

- Botón **Afterflow** en el menú principal y en la pausa.
- Panel táctil con etapas 1–7 y **OFF**, sin necesitar F6/F9.
- Selección guardada al tocar una etapa.
- Primer inicio en OFF si todavía no existe una selección guardada.
- Registro de sesión limitado a 32 eventos; **Logs** muestra los últimos cuatro.
- En iOS no se compilan los lanzadores de terminal, scripts, watcher de
  archivos ni avisos de actualización que enlazan a los binarios de escritorio.

La asistencia cambia el momento de los inputs. Las partidas asistidas no
deben presentarse como logros sin asistencia. El port conserva el motor de
predicción original; no promete precisión perfecta ni mejoras de rendimiento.

## Compilar

Se necesita macOS con Xcode y su SDK de iPhoneOS, CMake 3.29 o superior,
Geode CLI y Geode SDK 5.11.2 con sus binarios para iOS.

```sh
export GEODE_SDK=/ruta/al/geode-sdk
geode sdk install-binaries --platform ios --version v5.11.2
cmake -S . -B build-ios -DCMAKE_SYSTEM_NAME=iOS \
  -DGEODE_TARGET_PLATFORM=iOS -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DCMAKE_OSX_SYSROOT=iphoneos -DCMAKE_BUILD_TYPE=Release \
  -DGEODE_DONT_INSTALL_MODS=ON
cmake --build build-ios --parallel
python3 tools/verify_ios_package.py build-ios/afterflow.prsevend.geode
```

El workflow `Afterflow iOS` realiza la compilación en macOS y verifica que
el paquete contenga `afterflow.prsevend.ios.dylib`, ARM64 para iPhoneOS.
El artefacto de GitHub se llama **Afterflow-iOS**. Dentro del ZIP está el
archivo `.geode` que se instala; este proyecto fuente no es instalable.

## Primera prueba en iPhone

1. Comprueba las versiones exactas de GD y Geode antes de instalar.
2. Desactiva otros mods que cambien los inputs o la física durante la prueba.
3. Instala el `.geode` generado mediante el método de importación de tu
   Geode Launcher y reinicia el juego.
4. Comprueba que aparece el botón Afterflow en menú y pausa, que OFF conserva
   el control normal y que la selección persiste al reiniciar.
5. En una copia de nivel o en práctica, prueba etapas bajas, mantener/soltar,
   muerte/reinicio, pausa/reanudación, portales y dual.
6. Si falla, conserva el registro de Geode, las versiones exactas y los
   pasos para repetirlo. Una compilación exitosa no sustituye esta prueba.

Para iOS sin jailbreak, usa un Geode Launcher compatible con tu sistema.
El mod no instala ni configura el launcher ni modifica tu certificado.

## Referencias

- https://github.com/geode-sdk/docs/blob/main/misc/ios.md
- https://github.com/geode-sdk/geode/blob/v5.11.2/cmake/Platform.cmake
- https://github.com/geode-sdk/build-geode-mod
