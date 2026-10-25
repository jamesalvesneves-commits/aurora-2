# AURORA 2

Estúdio musical local para Windows, desenvolvido do zero; somente componentes gratuitos e livres, com Ardour e validação antes da versão master.

## Recursos

- Exportador MIDI offline
- Criação de sessão `.ardour` e importação de MIDI
- Abridor de sessão Ardour
- Fluxo integrado e CLI
- Integração OSC
- Instalador e documentação

## Versão 0.2.0

A versão `0.2.0` adiciona empacotamento Python, o comando `aurora2-studio` e build automatizado do executável Windows.

### Uso

```powershell
python -m aurora2 "Balada" tracks.json --root . --bpm 90 --ardour "C:\Program Files\Ardour8\bin\ardour8.exe" --open
```

### Build Windows

O workflow *Build Windows executable* gera o artefato `AURORA2-Windows-x64`, contendo `AURORA2.exe`.
