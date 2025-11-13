"""
Sistema de Backup Automatizado para Verint
Autor: Luciano Prado
Descrição: Script para backup automático com logs e notificações
"""

import os
import shutil
import configparser
import logging
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração de logging
def configurar_log():
    """Configura o sistema de logs"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    data_hoje = datetime.now().strftime("%Y%m%d")
    log_file = f'logs/backup_{data_hoje}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Carrega configurações
def carregar_config():
    """Carrega configurações do arquivo config.ini"""
    config = configparser.ConfigParser()
    
    if not os.path.exists('config.ini'):
        logging.error("Arquivo config.ini não encontrado!")
        criar_config_padrao()
        logging.info("Arquivo config.ini criado. Por favor, configure e execute novamente.")
        exit(1)
    
    config.read('config.ini', encoding='utf-8')
    return config

def criar_config_padrao():
    """Cria arquivo de configuração padrão"""
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'source_path': 'C:\\Verint\\Data',
        'backup_path': 'D:\\Backups',
        'retention_days': '30',
        'enable_email': 'False'
    }
    config['EMAIL'] = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': '587',
        'email_from': 'seuemail@gmail.com',
        'email_to': 'suporte@empresa.com',
        'email_password': ''
    }
    
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def executar_backup(source, destiny, logger):
    """Executa o backup e retorna informações"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"verint_backup_{timestamp}"
        backup_path = os.path.join(destiny, backup_name)
        
        logger.info(f"Iniciando backup de: {source}")
        logger.info(f"Destino: {backup_path}.zip")
        
        # Verifica se o diretório de origem existe
        if not os.path.exists(source):
            logger.error(f"Diretório de origem não encontrado: {source}")
            return None
        
        # Cria diretório de destino se não existir
        if not os.path.exists(destiny):
            os.makedirs(destiny)
            logger.info(f"Diretório de destino criado: {destiny}")
        
        # Executa o backup
        shutil.make_archive(backup_path, 'zip', source)
        
        # Calcula tamanho do backup
        backup_size = os.path.getsize(f"{backup_path}.zip") / (1024 * 1024)  # MB
        
        logger.info(f"Backup concluído com sucesso!")
        logger.info(f"Arquivo: {backup_name}.zip")
        logger.info(f"Tamanho: {backup_size:.2f} MB")
        
        return {
            'success': True,
            'filename': f"{backup_name}.zip",
            'size': backup_size,
            'path': f"{backup_path}.zip"
        }
        
    except Exception as e:
        logger.error(f"Erro durante o backup: {str(e)}")
        return {'success': False, 'error': str(e)}

def limpar_backups_antigos(destiny, retention_days, logger):
    """Remove backups mais antigos que o período de retenção"""
    try:
        logger.info(f"Verificando backups antigos (retenção: {retention_days} dias)")
        
        data_limite = datetime.now() - timedelta(days=int(retention_days))
        arquivos_removidos = 0
        
        for arquivo in os.listdir(destiny):
            if arquivo.endswith('.zip') and arquivo.startswith('verint_backup_'):
               caminho_completo = os.path.join(destiny, arquivo)
               data_arquivo = datetime.fromtimestamp(os.path.getctime(caminho_completo))            if data_arquivo < data_limite:
               os.remove(caminho_completo)
               arquivos_removidos += 1
               logger.info(f"Backup antigo removido: {arquivo}")    if arquivos_removidos > 0:
               logger.info(f"Total de backups antigos removidos: {arquivos_removidos}")
            else:
               logger.info("Nenhum backup antigo encontrado para remoção")except Exception as e:
               logger.error(f"Erro ao limpar backups antigos: {str(e)}")def enviar_notificacao_email(config, resultado, logger):
            """Envia notificação por email sobre o status do backup"""
      try:
    if config['DEFAULT'].get('enable_email', 'False') != 'True':
logger.info("Notificação por email desabilitada")
return    smtp_server = config['EMAIL']['smtp_server']
    smtp_port = int(config['EMAIL']['smtp_port'])
    email_from = config['EMAIL']['email_from']
    email_to = config['EMAIL']['email_to']
    email_password = config['EMAIL'].get('email_password', '')    
if not email_password:
        logger.warning("Senha de email não configurada. Notificação não enviada.")
        return

 # Prepara o email
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = f"Backup Verint - {'Sucesso' if resultado['success'] else 'Falha'}"
    
    if resultado['success']:
        corpo = f"""
        Backup executado com sucesso!
        
        Detalhes:
        - Arquivo: {resultado['filename']}
        - Tamanho: {resultado['size']:.2f} MB
        - Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        - Caminho: {resultado['path']}
        
        ---
        Sistema de Backup Automatizado - Verint
        """
    else:
        corpo = f"""
        ATENÇÃO: Falha no backup!
        
        Erro: {resultado.get('error', 'Erro desconhecido')}
        Data/Hora: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        
        Por favor, verifique os logs para mais detalhes.
        
        ---
        Sistema de Backup Automatizado - Verint
        """
    
        msg.attach(MIMEText(corpo, 'plain'))
    
    # Envia o email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_from, email_password)
        server.send_message(msg)
        server.quit()
    
        logger.info(f"Email de notificação enviado para: {email_to}")
    
    except Exception as e:
        logger.error(f"Erro ao enviar email: {str(e)}")

    def main():
        """Função principal"""
    # Configura logging
        logger = configurar_log()
        logger.info("="*60)
        logger.info("INICIANDO SISTEMA DE BACKUP AUTOMATIZADO")
        logger.info("="*60)

    # Carrega configurações
    config = carregar_config()
    source = config['DEFAULT']['source_path']
    destiny = config['DEFAULT']['backup_path']
    retention_days = config['DEFAULT']['retention_days']

    logger.info(f"Origem: {source}")
    logger.info(f"Destino: {destiny}")

    # Executa o backup
    resultado = executar_backup(source, destiny, logger)

    if resultado and resultado['success']:
    # Limpa backups antigos
        limpar_backups_antigos(destiny, retention_days, logger)
    
    # Envia notificação
        enviar_notificacao_email(config, resultado, logger)
    
        logger.info("="*60)
        logger.info("BACKUP FINALIZADO COM SUCESSO")
        logger.info("="*60)
    else:
        logger.error("="*60)
        logger.error("BACKUP FINALIZADO COM ERRO")
        logger.error("="*60)
    
    # Envia notificação de erro
        enviar_notificacao_email(config, resultado, logger)
    if name == "main":
    main()
