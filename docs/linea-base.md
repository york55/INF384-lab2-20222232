# Linea base de ejecucion

Ejecutar el workflow tres veces desde la pestana Actions, con **Run workflow**,
sin modificar ningun archivo del repositorio. Registrar aqui los resultados.

| Ejecucion | Duracion | URL |
|---|---|---|
| 1 |1m 7s  |https://github.com/york55/INF384-lab2-20222232/actions/runs/34487770724 |
| 2 |1m 11s |	https://github.com/york55/INF384-lab2-20222232/actions/runs/34488064644 |
| 3 |1m 4s  |	https://github.com/york55/INF384-lab2-20222232/actions/runs/34488246685 |

## Declaracion de uso de IA generativa

Indicar si se utilizaron herramientas de IA generativa para completar este
trabajo previo, cuales, y con que proposito. Adjuntar los prompts utilizados.

Me habían ocurrido errores al correr 2 veces el pipeline así que le pase el error para que me 
explique y lo que pasó es que había puesto las variables de organization y project_key 
como secrets, así que después de eso las cambie a variables

## Prompt

Run SonarSource/sonarqube-scan-action@v8
Installing Sonar Scanner CLI 8.1.0.6389 for linux-x64...
Downloading from: https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-8.1.0.6389-linux-x64.zip
Downloading signature from: https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-8.1.0.6389-linux-x64.zip.asc
Importing SonarSource public key from hkps://keyserver.ubuntu.com...
/usr/bin/gpg --homedir /home/runner/work/_temp/gpg-abc1f069 --batch --keyserver hkps://keyserver.ubuntu.com --recv-keys 679F1EE92B19609DE816FDE81DB198F93525EC1A
gpg: keybox '/home/runner/work/_temp/gpg-abc1f069/pubring.kbx' created
gpg: /home/runner/work/_temp/gpg-abc1f069/trustdb.gpg: trustdb created
gpg: key 1DB198F93525EC1A: public key "SonarSource S.A. <infra@sonarsource.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1
Successfully imported key from hkps://keyserver.ubuntu.com
✓ SonarSource public key imported successfully
Verifying GPG signature...
/usr/bin/gpg --homedir /home/runner/work/_temp/gpg-abc1f069 --batch --verify /home/runner/work/_temp/d5759abe-1d40-4a60-8fb9-29c37a084a67 /home/runner/work/_temp/158b3eaa-67a4-4d9e-ae84-8a142017ef03
gpg: Signature made Tue Apr 21 07:20:26 2026 UTC
gpg:                using RSA key D1436C0DBACEA48702AF97C363F1DD7753B8B315
gpg: Good signature from "SonarSource S.A. <infra@sonarsource.com>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 679F 1EE9 2B19 609D E816  FDE8 1DB1 98F9 3525 EC1A
     Subkey fingerprint: D143 6C0D BACE A487 02AF  97C3 63F1 DD77 53B8 B315
✓ GPG signature verification passed
/usr/bin/unzip -o -q /home/runner/work/_temp/158b3eaa-67a4-4d9e-ae84-8a142017ef03.zip
Sonar Scanner CLI cached to: /opt/hostedtoolcache/sonar-scanner-cli/8.1.0-build.6389/linux-x64
/opt/hostedtoolcache/sonar-scanner-cli/8.1.0-build.6389/linux-x64/bin/sonar-scanner -Dsonar.projectBaseDir=. -Dsonar.organization= -Dsonar.projectKey=
14:08:44.108 INFO  Scanner configuration file: /opt/hostedtoolcache/sonar-scanner-cli/8.1.0-build.6389/linux-x64/conf/sonar-scanner.properties
14:08:44.110 INFO  Project root configuration file: /home/runner/work/INF384-lab2-20222232/INF384-lab2-20222232/sonar-project.properties
14:08:44.121 INFO  SonarScanner CLI 8.1.0.6389
14:08:44.125 INFO  Linux 6.17.0-1022-azure amd64
14:08:46.482 INFO  Communicating with SonarQube Cloud
14:08:46.482 INFO  JRE provisioning: os[linux], arch[x86_64]
14:08:49.600 INFO  Starting SonarScanner Engine...
14:08:49.600 INFO  Java 21.0.12.1 Eclipse Adoptium (64-bit)
14:08:52.040 INFO  Load global settings
14:08:52.835 INFO  Load global settings (done) | time=790ms
14:08:52.910 INFO  Server id: 1BD809FA-AWHW8ct9-T_TB3XqouNu
14:08:53.063 INFO  Loading required plugins
14:08:53.065 INFO  Load plugins index
14:08:53.238 INFO  Load plugins index (done) | time=173ms
14:08:53.238 INFO  Load/download plugins
14:08:53.814 INFO  Load/download plugins (done) | time=575ms
14:08:54.082 INFO  Loaded core extensions: a3s, architecture, sca
14:08:54.312 INFO  Load project settings for component key: ''
14:08:54.499 INFO  Failed to load settings with NOT_FOUND error, which can happen if the project does not exist yet
14:08:54.511 INFO  Found an active CI vendor: 'Github Actions'
14:08:54.892 INFO  Process project properties
14:08:54.945 ERROR Validation of project reactor failed:
  o "" is not a valid project or module key. It cannot be empty nor contain whitespaces.
14:08:55.264 INFO  EXECUTION FAILURE
14:08:55.265 INFO  Total time: 11.158s
Error: Action failed: The process '/opt/hostedtoolcache/sonar-scanner-cli/8.1.0-build.6389/linux-x64/bin/sonar-scanner' failed with exit code 3
