# Auditoria de licenças — Estágio 1

Data da auditoria: 23/10/2026.

## Regra

Um componente só pode entrar no stack master se for 100% gratuito e utilizável sem trial, limite de uso, exigência de cartão de crédito ou restrição não comercial.

## Aprovados

| Componente | Licença / base legal | Decisão |
|---|---|---|
| Ollama | MIT | Aprovado. |
| Qwen2.5-Coder 7B / 7B-Instruct | Apache-2.0 | Aprovado. Usar variante 7B, não a 72B. |
| Continue.dev | Apache-2.0 | Aprovado. |
| Ardour | GPL; compilação a partir do código-fonte | Aprovado como DAW central. |
| Audacity | GPLv3, com arquivos GPLv2+ | Aprovado. |
| LMMS | GPL-2.0-or-later | Aprovado. |
| Zrythm | AGPL-3.0 | Aprovado. |
| OpenMPT | BSD-3-Clause | Aprovado. |
| Surge XT | GPL-3.0 | Aprovado. |
| Vital — código-fonte | GPLv3 | Aprovado somente como build próprio do código-fonte. |
| FluidSynth | LGPL-2.1 | Aprovado. |
| Bespoke Synth | GPLv3 | Aprovado. |
| Cardinal | GPLv3+ | Aprovado. |
| ACE-Step 1.5 | MIT, código e modelo oficial | Aprovado. |
| StemDeck | Apache-2.0 | Aprovado como interface de separação. |
| FFmpeg | LGPL-2.1+; build GPL opcional | Aprovado. Usar build compatível com a distribuição do AURORA 2. |

## Aprovados com ressalva

| Componente | Ressalva |
|---|---|
| Vital | O código é GPLv3, mas presets, samples, wavetables e skins distribuídos pela Vital Audio têm licença separada. O AURORA 2 deve compilar o Vital e não redistribuir conteúdo oficial não licenciado para redistribuição. |
| Cardinal | O binário é GPLv3+, mas parte das artes/módulos do ecossistema VCV possui licenças separadas, incluindo CC BY-NC. Usar a distribuição oficial Cardinal e não redistribuir artes restritas. |
| FFmpeg | A licença depende das opções de compilação. Registrar exatamente qual build será usado e suas licenças. |
| StemDeck | O projeto é Apache-2.0, mas depende de modelos e FFmpeg de licenças próprias. Validar cada dependência empacotada. |

## Excluídos

| Componente | Motivo |
|---|---|
| MusicGen — pesos oficiais | CC-BY-NC 4.0; uso não comercial. |
| Stable Audio Open | Licença não comercial da Stability AI. |
| Qwen2.5-Coder 72B | Usa licença Qwen com restrições; não será usado. |

## Pendência crítica

| Item | Situação |
|---|---|
| Pesos do Demucs, incluindo `htdemucs_6s` | O código do Demucs é MIT, mas os pesos pré-treinados têm condições separadas e podem ser destinados principalmente à pesquisa. O AURORA 2 não pode declarar o separador de stems aprovado até confirmar a licença exata dos pesos utilizados. |

## Consequência para o stack

- O módulo de separação de stems permanece em desenvolvimento, mas não é considerado aprovado para a versão master enquanto os pesos do Demucs não forem validados.
- Se os pesos `htdemucs_6s` não forem compatíveis, o AURORA 2 deverá substituir o modelo por alternativa com licença 100% livre ou implementar separação sem esses pesos.
