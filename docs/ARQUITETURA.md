# Arquitetura AURORA 2

## Princípio

O AURORA 2 é um **orquestrador local**. Ele coordena ferramentas musicais reais, mas não substitui suas interfaces originais.

## Camadas

1. **Interface central** — PySide6, Python 3.11.9.
2. **Orquestrador local** — Ollama interpreta prompts em português e produz planos estruturados.
3. **Camada de desenvolvimento** — Qwen2.5-Coder, Continue.dev, Git e GitHub CLI.
4. **Camada de produção musical** — Ardour, Audacity, LMMS, Zrythm, OpenMPT e ferramentas de síntese.
5. **Camada de IA musical** — somente modelos e projetos com licença compatível com uso livre.
6. **Camada de áudio** — Demucs, StemDeck, FFmpeg, SoX, FluidSynth e gravação de voz.
7. **Camada de exportação** — WAV e MP3, com metadados e organização por projeto.

## Regras de integração

- Cada componente é aberto pela interface original.
- O Ardour é controlado por OSC e permanece editável pelo mouse.
- Scripts gerados pela IA exigem visualização, edição e aprovação antes da execução.
- Nenhuma integração é declarada concluída sem validação em ambiente Windows real.
- Componentes com licença incompatível são removidos do stack, não simulados.
