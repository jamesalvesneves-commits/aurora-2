# Plano Ardour no AURORA 2

## Decisão

O Ardour permanece como DAW central do AURORA 2.

## Problema no Windows

Os binários oficiais de teste/demo do Ardour para Windows podem interromper o áudio periodicamente. Isso é inaceitável para o AURORA 2.

## Solução obrigatória

O AURORA 2 não usará a edição demo como versão final. O Ardour será compilado a partir do código-fonte para Windows, de forma reproduzível, para produzir um binário sem a limitação da edição demo.

## Estágios de validação

1. Documentar o processo oficial de build do Ardour para Windows.
2. Preparar ambiente de compilação isolado e reproduzível.
3. Compilar o Ardour a partir do código-fonte.
4. Testar criação, reprodução, gravação, exportação e salvamento de sessão.
5. Confirmar ausência da limitação da edição demo.
6. Criar sessão `.ardour` automaticamente pelo AURORA 2.
7. Criar faixas MIDI e áudio automaticamente.
8. Importar arquivos gerados para a sessão.
9. Controlar transporte, volume, pan, mute e solo via OSC.
10. Validar edição manual completa pelo mouse no Ardour.

## Critério de aceite

O Ardour só será considerado integrado quando uma sessão criada pelo AURORA 2 puder ser aberta, editada, reproduzida, salva e exportada no Windows sem a limitação da edição demo.
