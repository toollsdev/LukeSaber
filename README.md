# Luke's Saber

**Luke's Saber** é um bot de música de alta fidelidade para Discord, projetado para trazer reprodução ágil, áudio cristalino e integração fluida com múltiplas plataformas diretamente para os seus canais de voz.

Mantido por **[toollsdev](https://github.com/toollsdev)** · [Repositório](https://github.com/toollsdev/lukesaber) · [Relatar um problema](https://github.com/toollsdev/lukesaber/issues)

## Recursos

- Player interativo com botões, comandos de barra e comandos por prefixo.
- Fila de músicas, playlists, pausa, retomada, volume e repetição.
- Reprodução de vídeos do YouTube pela fonte exata, sem trocar automaticamente por covers de outras plataformas.
- Integração com links e metadados do Spotify e suporte a fontes como SoundCloud.
- Player fixo em canal de pedidos, skins personalizáveis e suporte a múltiplos bots.
- Integração opcional com Last.fm e Rich Presence.
- Aviso no terminal quando a autorização do YouTube precisar ser renovada, quando o Lavalink for iniciado pelo bot.

O Spotify fornece os metadados das faixas; a reprodução depende de uma fonte de áudio compatível. A disponibilidade e a qualidade final também dependem da fonte e do servidor de música.

## Stack

Python · Disnake · Wavelink customizado · Lavalink · youtube-source · LavaSrc

## Instalação

Tenha Python 3.11 ou superior, Git e um JDK compatível com a versão do Lavalink utilizada.

```bash
git clone https://github.com/toollsdev/lukesaber.git
cd lukesaber
python -m venv venv
```

Ative o ambiente no Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Ou no Linux:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Configuração

Copie [`.example.env`](.example.env) para `.env` na raiz do projeto e preencha suas credenciais. O exemplo contém as opções comentadas, sem tokens ou senhas reais.

No PowerShell:

```powershell
Copy-Item .example.env .env
```

Se você já tem um `.env` configurado, mantenha-o e consulte o exemplo sem sobrescrevê-lo. Configuração inicial para um servidor Lavalink local iniciado pelo bot:

```dotenv
TOKEN_BOT_1=seu_token_do_discord
DEFAULT_PREFIX=!
SOURCE_REPO=https://github.com/toollsdev/lukesaber.git
RUN_LOCAL_LAVALINK=true
CONNECT_LOCAL_LAVALINK=true
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

Use o [Discord Developer Portal](https://discord.com/developers/applications) para criar a aplicação, obter o token e configurar as permissões e intents necessárias. Convide o bot com os escopos `bot` e `applications.commands`, permitindo acesso aos canais de texto e voz.

As opções disponíveis ficam em [`config_loader.py`](config_loader.py). Mantenha tokens e segredos apenas nos arquivos locais; não os publique no GitHub.

### YouTube e Lavalink

O servidor utiliza o plugin `youtube-source`. No `application.yml`, a fonte interna antiga do YouTube deve ficar desativada e o plugin deve estar habilitado.

Se a configuração exigir autorização, conclua o fluxo do Google mostrado pelo Lavalink e salve o `refreshToken` na configuração local para reutilizá-lo nas próximas inicializações.

Esta versão inclui uma [correção local de leitura por blocos](lavalink_patches/youtube-range-length/README.md), validada com youtube-source 1.18.2 e Lavaplayer 2.2.7. O JAR modificado é um arquivo local: siga o procedimento de reconstrução após uma instalação nova. Atualizações do plugin podem remover a correção.

### Spotify

Obtenha o Client ID e o Client Secret no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard). Preencha `SPOTIFY_CLIENT_ID` e `SPOTIFY_CLIENT_SECRET` no `.env`.

Para a integração via LavaSrc, configure também `plugins.lavasrc.spotify.clientId` e `plugins.lavasrc.spotify.clientSecret` no `application.yml`, com a fonte Spotify habilitada. Reinicie os processos correspondentes após alterar suas configurações. O acesso à API depende das regras e permissões vigentes do Spotify.

## Executar

Com o ambiente ativado:

```bash
python main.py
```

No Windows, também é possível usar `source_start_windows.bat`.

Entre em um canal de voz e use os comandos de música do bot. Use `/setup` para configurar o player fixo e `/change_skin` para escolher sua aparência.

## Diagnóstico

- Logs do servidor de música: `.logs/lavalink/spring.log`.
- **VOCÊ PRECISA RENOVAR O TOKEN**: conclua novamente a autorização do YouTube e atualize o token local.
- Erros de leitura ou decodificação de áudio não significam necessariamente que o token expirou.
- Ao abrir uma issue, informe o comando, a fonte, as versões e o erro, removendo tokens e dados privados.

## Manutenção e licença

**Luke's Saber** é a versão personalizada mantida por **toollsdev**, baseada no projeto MuseHeart-MusicBot, de zRitsu. A personalização não altera a autoria do código preexistente.

Os avisos originais permanecem em [`LICENSE`](LICENSE). O projeto mantém a licença GNU GPL indicada nesse arquivo; bibliotecas e componentes externos conservam suas próprias licenças.
