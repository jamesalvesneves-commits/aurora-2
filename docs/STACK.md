# Stack AURORA 2

## Regra de aceite

Um componente só entra no stack master se for:

- 100% gratuito para o uso previsto;
- open-source ou de licença compatível;
- utilizável sem cartão de crédito, trial, limite de uso ou restrição não comercial;
- compatível com Windows 11 e com o hardware-alvo;
- integrável de forma real, testável e documentada.

## Status após o Estágio 1

| Componente | Licença / decisão | Status |
|---|---|---|
| Aurora Studio | Projeto próprio, GPL-3.0 | A construir |
| Ollama | MIT | Aprovado |
| Qwen2.5-Coder 7B | Apache-2.0 | Aprovado |
| Continue.dev | Apache-2.0 | Aprovado |
| Git for Windows | GPLv2 | Aprovado |
| GitHub CLI | MIT | Aprovado |
| Chocolatey | Apache-2.0 / GPL compatível | A validar build e fontes |
| Ardour | GPL; build próprio no Windows | Aprovado como DAW central |
| Audacity | GPLv3 | Aprovado |
| LMMS | GPL-2.0-or-later | Aprovado |
| Zrythm | AGPL-3.0 | Aprovado |
| OpenMPT | BSD-3-Clause | Aprovado |
| Surge XT | GPL-3.0 | Aprovado |
| Vital | GPLv3 no código-fonte | Aprovado somente via build próprio |
| FluidSynth | LGPL-2.1 | Aprovado |
| Bespoke Synth | GPLv3 | Aprovado |
| Cardinal | GPLv3+ | Aprovado com ressalva de artes/módulos |
| ACE-Step 1.5 | MIT | Aprovado |
| StemDeck | Apache-2.0 | Aprovado com ressalva de dependências |
| Demucs | Código MIT; pesos pendentes | Bloqueado até validação dos pesos |
| SoX | LGPL/GPL conforme build | A validar build exato |
| FFmpeg | LGPL-2.1+ / GPL opcional | Aprovado com ressalva de build |
| Módulo de letras | Projeto próprio | A construir |
| Módulo de harmonia | Projeto próprio | A construir |
| Módulo de ritmo | Projeto próprio | A construir |
| Módulo de melodia | Projeto próprio | A construir |
| Gravação de voz | Projeto próprio | A construir |
| Importação de áudio/MIDI | Projeto próprio | A construir |
| Exportador WAV/MP3 | Projeto próprio | A construir |

## Excluídos definitivamente

| Componente | Motivo |
|---|---|
| MusicGen — pesos oficiais | CC-BY-NC 4.0; uso não comercial. |
| Stable Audio Open | Licença não comercial da Stability AI. |
| Qwen2.5-Coder 72B | Licença Qwen com restrições; substituído pela variante 7B Apache-2.0. |

## Próxima validação

1. Confirmar a licença exata dos pesos `htdemucs_6s` do Demucs.
2. Escolher e documentar o build do FFmpeg e do SoX.
3. Definir o processo de build do Vital a partir do código-fonte.
4. Confirmar fontes e licenças do Chocolatey.
5. Documentar o processo de compilação do Ardour para Windows.
