# Instalação do AURORA 2

## Requisitos

- Windows 11 Pro.
- Python 3.11.9.
- Git for Windows.
- GitHub CLI.
- Ollama.
- FFmpeg no PATH.
- GPU NVIDIA recomendada; o sistema também pode operar em CPU, com desempenho menor.

## Instalação base

No PowerShell, dentro da pasta clonada do repositório:

```powershell
git clone https://github.com/jamesalvesneves-commits/aurora-2.git
cd aurora-2
python scripts\install_aurora2.py
```

O instalador:

1. Detecta Python, GPU, RAM, Ollama, FFmpeg, Git e GitHub CLI.
2. Cria a estrutura local em `%USERPROFILE%\AURORA2`.
3. Instala as dependências Python do `requirements.txt`.
4. Reutiliza downloads já existentes quando o arquivo de destino já existe.
5. Cria o atalho `AURORA 2.bat` na área de trabalho.
6. Informa pendências em vez de fingir que tudo foi instalado.

## Verificação

```powershell
python scripts\detect_environment.py
```

## Limites deste estágio

Este estágio instala e valida o **ambiente base**. Ele ainda não instala automaticamente Ardour, DAWs, sintetizadores, modelos musicais ou realiza a integração completa de produção.

O Ardour será integrado somente após a conclusão e validação do processo de compilação própria para Windows, sem a limitação da edição demo.
