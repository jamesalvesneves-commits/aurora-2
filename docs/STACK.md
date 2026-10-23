# Stack AURORA 2

## Regra de aceite

Um componente só entra no stack master se for:

- 100% gratuito para o uso previsto;
- open-source ou de licença compatível;
- utilizável sem cartão de crédito, trial, limite de uso ou restrição não comercial;
- compatível com Windows 11 e com o hardware-alvo;
- integrável de forma real, testável e documentada.

## Mantidos

| Componente | Papel | Situação |
|---|---|---|
| Aurora Studio | Interface central PySide6 | A construir |
| Ollama | Orquestrador LLM local | A validar |
| Qwen2.5-Coder | Modelo de código local | A validar licença e pesos |
| Continue.dev | Assistente de código no VS Code | A validar |
| Git for Windows | Versionamento | A instalar |
| GitHub CLI | Automação GitHub | A instalar |
| Chocolatey | Instalação de dependências | A validar |
| Ardour | DAW central | Mantido; compilação própria no Windows |
| Audacity | Edição e gravação | A validar |
| LMMS | Produção eletrônica e MIDI | A validar |
| Zrythm | DAW MIDI-first | A validar |
| OpenMPT | Tracker e composição modular | A validar |
| Surge XT | Sintetizador VST3 | A validar |
| Vital | Sintetizador wavetable | A validar licença da edição usada |
| FluidSynth | Sintetizador MIDI/SoundFont | A validar |
| Bespoke Synth | Ambiente modular | A validar |
| Cardinal | Modular VCV | A validar |
| ACE-Step | Geração musical por IA | Candidato; validar licença e VRAM |
| StemDeck | Separação de stems | A validar |
| Demucs | Motor de separação | A validar licença e pesos |
| SoX | Processamento de áudio | A validar |
| FFmpeg | Conversão e processamento | A validar |
| Módulo de letras | Geração em português | A construir |
| Módulo de harmonia | Acordes e progressões | A construir |
| Módulo de ritmo | Bateria e groove | A construir |
| Módulo de melodia | Melodias e linhas | A construir |
| Gravação de voz | Captura de microfone | A construir |
| Importação de áudio/MIDI | WAV, MP3, FLAC, MIDI | A construir |
| Exportador WAV/MP3 | Renderização final | A construir |

## Excluídos por licença

| Componente | Motivo |
|---|---|
| MusicGen — pesos oficiais | Pesos licenciados como CC-BY-NC 4.0, uso não comercial. |
| Stable Audio Open | Licença não comercial da Stability AI. |

## Pendências de validação

- Confirmar licença exata e pesos utilizáveis do Qwen2.5-Coder.
- Confirmar licença e binários gratuitos do Vital.
- Confirmar licença, pesos e execução do Demucs/StemDeck.
- Confirmar se o ACE-Step atende à exigência de licença livre e roda no hardware-alvo.
- Definir o processo reproducível de compilação do Ardour para Windows.
