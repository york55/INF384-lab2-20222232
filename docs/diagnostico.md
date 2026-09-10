## 1.1 Los cuatro defectos

### El pipeline utiliza requirements.txt (que contiene rangos abiertos) y no el requirements.lock
- Los steps Instalar dependencias en los jobs validar y publicar corren
  "pip install -r requirements.txt". "requirements.txt" declara rangos abiertos,
  por ejemplo, "requests>=2.31", no versiones fijas. El repositorio si tiene un archivo
  requirements.lock con versiones exactas, pero el pipeline no lo usa.
- El archivo del error es ".github/workflows/pipeline.yml", en las lineas 23-26
  y 53-56.
- Debido a esto no se puede reproducir el build. Dos ejecuciones en fechas
  distintas pueden resolver versiones distintas de las mismas dependencias sin que
  nadie haya tocado el codigo, por lo que un mismo commit puede pasar hoy y fallar
  manana.

### El pipeline no cachea las dependencias entre ejecuciones
- Ni el step Preparar Python (actions/setup-python) declara cache: pip, ni hay
  ningun step de actions/cache en ninguno de los dos jobs. Cada ejecucion vuelve a
  descargar y resolver todas las dependencias desde cero.
- El archivo del error es ".github/workflows/pipeline.yml", en las lineas 23-26
  y 53-56.
- Debido a esto el tiempo de instalacion se repite completo en cada job y en
  cada corrida, sin ningun ahorro entre ejecuciones consecutivas.

### El analisis de calidad no detiene el pipeline si el quality gate falla
- El step Analisis de calidad (SonarSource/sonarqube-scan-action@v8) envia el
  codigo a SonarCloud para analisis, pero no hay ningun step despues que espere o
  verifique el resultado del quality gate.
- El archivo del error es ".github/workflows/pipeline.yml", en las lineas 31-39.
- Debido a esto el analisis de calidad es meramente informativo. El quality gate
  puede marcar Failed en SonarCloud y el job de GitHub Actions termina en verde de
  todas formas.

### El job publicar corre sin depender de la validacion, sin restriccion de rama, y sin version en el nombre
- El job publicar no declara needs: validar (corre en paralelo, sin esperar a que
  la validacion pase), no tiene ningun if que lo restrinja a la rama main, y el
  artefacto se nombra simplemente "paquete", sin ninguna version.
- El archivo del error es ".github/workflows/pipeline.yml", en las lineas 41-66,
  especificamente la ausencia de needs/if y el nombre en la línea 64.
- Debido a esto se puede publicar un artefacto sin que haya pasado ninguna
  validacion, desde cualquier rama, y sin poder identificar que version es.

## 1.2 El defecto que explica la duracion

El defecto de la falta de cache explica el tiempo registrado en docs/linea-base.md
(1m4s, 1m7s, 1m11s en las tres corridas). Para un proyecto de este tamaño, ese
tiempo es en su mayoria instalacion de dependencias por red, repetida completa en
cada job y en cada corrida, sin nada cacheado.

## 1.3 El vinculo con el caso
CASO 2: Financiera Los Andes

El defecto que ataca la restriccion real del caso es el defecto 3 (el analisis de calidad no detiene el
pipeline). La automatizacion de Financiera Los Andes es rapida, ya que el pipeline corre en
35 minutos, pero eso no es lo que traba el flujo. El control real de calidad y
seguridad ocurre tarde y de forma manual, en la revision de Seguridad de la
Informacion (SLA interno de 5 dias habiles) y en el Comite de Cambios (espera
semanal).

Dato del value stream map que lo sustenta: en el trimestre se encontraron 14
hallazgos de seguridad en la revision manual, de los cuales 11 corresponden a
librerias de terceros desactualizadas. Ese es el tipo de hallazgo que un
quality gate automatizado detectaria en minutos dentro del pipeline.


## 1.4 La metrica DORA

De las cuatro métricas DORA, las alcanzables sin desplegar son:
- Lead Time for Changes: tiempo desde el commit hasta que el codigo esta listo
  para produccion. La duracion del pipeline es parte directa de esto.
- Change Failure Rate: porcentaje de cambios que llegan a main y causan
  problemas. El quality gate deteniendo versiones invalidas ataca esto
  directamente.

Para este caso se escogería Lead Time for Changes, ya que es la metrica que la propia 
corrección de los errores actuales puede mover de forma medible: el defecto 2 identificado en 1.2 
(falta de cache) aumenta directamente la duracion del pipeline, que es un componente del lead time.
Corrigiendo ese defecto se puede demostrar una reducción medible.

## 1.5 El proxy

El proxy es la duracion total del pipeline: el mismo numero que ya se registro en
linea-base.md (1m4s, 1m7s, 1m11s), medido de nuevo despues de corregir el defecto 2
(cache de dependencias).
