# ADR 0001 — Ardour gratuito para Windows

Data: 2026-10-24
Status: decisão proposta; compilação e testes ainda pendentes.

## Reinício

A nova implementação será escrita sem reutilizar código, scripts, testes ou configuração do Aurora anterior. Este registro não valida os arquivos já existentes em development e não importa material de outro projeto. Nenhum histórico será apagado sem autorização específica.

## Estado observado

- development: 0225890058aa40bf346d6b9d6968a6c0be71366f.
- main: 3958e3c06accbedac41900a16a9e00699c7c77be; contém README.md. A afirmação anterior de que main estava vazia estava incorreta.
- Esta alteração acrescenta somente documentação; não instala nem executa software.

## Decisão

Ardour permanece como DAW central. Investigar primeiro a compilação cruzada Linux/MinGW usada pelo projeto oficial, com saída Windows x86_64. Não prometer compilação nativa MSYS2 como solução já comprovada. Não usar a edição demo como distribuição final.

## Evidência primária

- https://ardour.org/faq.html — código-fonte gratuito; binários prontos oferecidos mediante pagamento; descreve compilação cruzada Linux/MinGW.
- https://github.com/Ardour/ardour/blob/master/tools/x-win/compile.sh — script oficial; aceita XARCH=x86_64 e depende de PREFIX com a pilha de bibliotecas preparada.
- https://ardour.org/current_dependencies.html — dependências devem incluir as versões modificadas exigidas pelo projeto.

## Trabalho necessário antes de automatizar

1. Fixar commit/tag do Ardour e do conjunto oficial de ferramentas de build.
2. Identificar e revisar o processo completo de construção das dependências; o script compile.sh isolado não basta.
3. Registrar fontes, versões, licenças e hashes das dependências.
4. Preparar ambiente Linux isolado; não presumir que WSL ou Docker já foram validados.
5. Compilar para Windows x86_64 e empacotar bibliotecas, recursos e avisos de licença.
6. Gerar hash SHA-256, logs e manifesto do artefato.

## Aceite obrigatório em Windows 11

- Executável abre sem DLLs ausentes e preserva a interface original.
- Reprodução de áudio por pelo menos 30 minutos sem silêncio periódico da demo.
- Captura de microfone, MIDI, salvamento, reabertura e exportação WAV funcionam.
- Controle OSC: transporte, volume, pan, mute e solo com confirmação observável.
- Sessão criada pela automação importa áudio/MIDI e permanece editável com mouse.
- Testes registram versão do Windows, dispositivo de áudio, resultado e logs.

## Limites

Nenhum binário foi compilado ou testado nesta auditoria. O conector GitHub permite operações no repositório, mas não constitui acesso ao Windows do usuário. Um commit de documentação não comprova integração nem versão master. A main não será alterada por esta operação.
