## 1.1 Los cuatro defectos

### El pipeline utiliza requirements.txt (que contiene rangos abiertos) y no el requirements.lock
- Los steps Instalar dependencias en los jobs validar y publicar corren
  "pip install -r requirements.txt". Este "requirements.txt" declara rangos abiertos,
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

## 4.1 Medición posterior

Proxy declarado: duracion total del pipeline.

- Antes de la intervención: 1m4s, 1m7s, 1m11s (promedio = 67s).
- Después de la intervención: 1m19s, 1m29s, 1m17s (promedio = 82s).

El proxy subio, no bajo: un incremento de aproximadamente 15 segundos.

Esto no significa que el defecto 2 no se haya resuelto: el step "Instalar
dependencias" si bajo notablemente al comparar ejecuciones consecutivas. Lo que
subio el total fueron dos efectos nuevos introducidos al corregir los defectos 3 y 4:
Primero, needs: validar obliga a que los jobs corran en secuencia en vez de en paralelo,
sumando sus duraciones en vez de solaparse.
Segundo, el nuevo step de verificación del quality gate depende de un servicio externo 
(SonarCloud), cuyo tiempo de respuesta (43s observados) varia entre ejecuciones y 
no se puede cachear. El proxy elegido mide el efecto agregado de todo el pipeline, y 
ese agregado empeoro aunque el componente de instalación si mejoro.

## 4.2 Justificacion de la version

Version declarada: 1.3.0 (desde 1.2.0).

Commits desde el tag v1.2.0:
- feat(tarifas): agregar desglose de la tarifa calculada
- fix(validaciones): colapsar espacios repetidos en el nombre del cliente
- fix(tarifas): redondear el costo por peso a dos decimales
- ci: pipeline de validacion y publicacion de artefacto
- fix: pipeline sonar project key como constante y sonar org pasando a github
  variable (dos commits)
- fix: borrando archivo .DS_Store
- fix: sonar project key

## 4.3 Qué no se resolvio

El defecto 2 solo cachea las dependencias de pip, pero no cachea el binario del
Sonar Scanner CLI. En los logs de Analisis de calidad se ve que cada ejecucion
descarga de nuevo el CLI completo (Installing Sonar Scanner CLI 8.1.0..., Downloading
from https://binaries.sonarsource.com/...).

Para resolverlo haria falta un step de actions/cache explicito, con una clave basada
en la version del scanner, que guarde el directorio donde
se descarga el binario entre ejecuciones --. Sin eso, parte del tiempo de "Analisis de calidad" seguira
dependiendo de una descarga por red en cada corrida.

## 4.4 Declaración de uso de IA generativa
Se utilizo Claude pro, mediante los siguientes prompts

1. Estoy trabajando en mi repositorio https://github.com/york55/INF384-lab2-20222232 que
   utilicé para mi lab previo, necesito que detectes que errores pueden existir en el pipeline.yml
   
2. okey ahora necesito que resuelvas los conflictos que detectaste siguiendo las siguientes condiciones
1 Las dependencias se instalan desde el archivo de bloqueo, no resolviendo versiones 2 Las dependencias se
cachean entre ejecuciones 3 El pipeline se detiene si el análisis de calidad no cumple el quality gate 4
El artifact publicado debe llamarse despachos-, solo desde main, y solo si la validación pasó

3. Necesito que me generes una función nueva de al menos 15 líneas, con lógica real —condicionales, no un return fijo— y sin
ninguna prueba que la cubra en un archivo existente de src/despachos/

4. Como se podría solucionar la demora que existe en la parte de "Analisis de calidad" de mi pipeline en Validar?
