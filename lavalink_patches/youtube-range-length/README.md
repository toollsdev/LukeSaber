# Correção local da leitura por blocos do YouTube

Aplicada sobre **youtube-source 1.18.2**, testada com **Lavaplayer 2.2.7**.

Quando o formato 18 não informa o tamanho total, `PersistentHttpStream`
interpreta o `Content-Length` da primeira resposta parcial como o tamanho
do vídeo completo. Isso pode interromper a reprodução depois do primeiro
bloco de aproximadamente 11,8 MB, inclusive ao avançar na faixa.

A alteração em `createContentInputStream` impede essa inferência para blocos
completos. Um bloco menor que o solicitado informa o fim do recurso; nesse
caso o tamanho inclui a posição inicial do bloco. Tamanhos já conhecidos e
URLs de streaming com `rn=` mantêm o comportamento original.

Fonte original: https://github.com/lavalink-devs/youtube-source/blob/1.18.2/common/src/main/java/dev/lavalink/youtube/track/YoutubePersistentHttpStream.java

## Reconstruir

No PowerShell, a partir da raiz do projeto, com um JDK instalado:

```powershell
./lavalink_patches/youtube-range-length/build.ps1 -JdkDirectory 'C:\Program Files\Java\jdk-26'
```

O script compila e executa os testes sem rede e produz o JAR em
`.tmp/youtube-range-build/youtube-plugin-1.18.2.jar`.
Ele não reinicia o servidor nem substitui o plugin instalado.
Para aplicar, pare o Lavalink, guarde uma cópia do plugin anterior e
substitua `plugins/youtube-plugin-1.18.2.jar` pelo arquivo produzido.

Uma atualização ou reinstalação do plugin oficial pode remover esta correção.
Reavalie sua necessidade ao mudar a versão; não aplique automaticamente a
versões diferentes da 1.18.2.

## Verificação

`RangeLengthTest.java` verifica tamanho desconhecido, tamanho total no último
bloco, tamanho conhecido e URLs de streaming. Os testes não usam credenciais.
O teste de integração foi realizado separadamente com o vídeo
`N31mWYiB3gU`, incluindo retomada em 137680 ms.
