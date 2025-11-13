# 🤖 Automação de Backup - Python

Sistema automatizado de backup para plataformas Verint, desenvolvido para uso em ambiente de produção. Inclui sistema de logs, notificações e configuração via arquivo INI.

## 🎯 Características

- ✅ Backup automatizado com compactação ZIP
- ✅ Sistema de logs com timestamp
- ✅ Configuração externa via arquivo `.ini`
- ✅ Notificação de status por email (opcional)
- ✅ Limpeza automática de backups antigos
- ✅ Compatível com Windows Server

## 📁 Estrutura do Projeto
```
automacao-backup-python/
├── backup_verint.py       # Script principal
├── config.ini             # Configurações
├── requirements.txt       # Dependências
├── logs/                  # Pasta de logs (gerada automaticamente)
└── README.md
```

## 🚀 Como Usar

### 1. Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/automacao-backup-python.git

# Entre na pasta
cd automacao-backup-python

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração

Edite o arquivo `config.ini`:
```ini
[DEFAULT]
source_path = C:\Verint\Data
backup_path = D:\Backups
retention_days = 30
enable_email = False

[EMAIL]
smtp_server = smtp.gmail.com
smtp_port = 587
email_from = seuemail@gmail.com
email_to = suporte@empresa.com
```

### 3. Execução
```bash
python backup_verint.py
```

### 4. Agendamento (Windows)

Agende via Task Scheduler para executar diariamente:
- Abra o Agendador de Tarefas
- Crie Nova Tarefa Básica
- Configure para executar: `python C:\caminho\backup_verint.py`

## 📊 Logs

Os logs são salvos em `logs/backup_YYYYMMDD.log` com informações:
- Timestamp de início e fim
- Tamanho do backup gerado
- Status de sucesso/erro
- Backups removidos (limpeza automática)

## 🔧 Tecnologias Utilizadas

- Python 3.8+
- Bibliotecas: shutil, configparser, smtplib, logging

## ⚠️ Observações

Este script foi desenvolvido para ambientes Windows Server com SQL Server e é baseado em experiência real de produção na Mutant (2017-2025).

## 👤 Autor

**Luciano Prado**  
[LinkedIn](https://www.linkedin.com/in/lucianolacerdaprado) | [Email](mailto:lucianolpo@hotmail.com)
