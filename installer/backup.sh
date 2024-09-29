#!/bin/bash
# 设置变量
DB_NAME="maxkb"  # 替换为您的数据库名称
BACKUP_DIR="/model/postgres/backup/$(date +%Y-%m-%d_%H-%M-%S)"  # 备份目录
DB_USER="root"  # 数据库用户
LOG_FILE="/model/postgres/backup/backup.log"  # 日志文件
PG_CTL_PATH="/usr/lib/postgresql/15/bin/pg_ctl"  # 替换为您的 pg_ctl 实际路径
PG_PID_FILE="/var/lib/postgresql/data/postmaster.pid"  # 替换为您的实际路径

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 获取 PostgreSQL 数据存放位置
DATA_DIR=$(psql -U "$DB_USER" -d "$DB_NAME" -c "SHOW data_directory;" | awk 'NR==3 {print $1}')
echo "PostgreSQL data directory: $DATA_DIR" | tee -a "$LOG_FILE"

# 检查是否成功获取数据目录
if [ -z "$DATA_DIR" ]; then
    echo "Failed to get PostgreSQL data directory." | tee -a "$LOG_FILE"
    exit 1
fi

# 删除一周前的备份文件
echo "Deleting backups older than 7 days from $BACKUP_DIR..." | tee -a "$LOG_FILE"
find /model/postgres/backup/* -type d -mtime +7 -exec rm -rf {} + 2>> "$LOG_FILE"

# 停止 PostgreSQL 服务
if [ -f "$PG_PID_FILE" ]; then
    PG_PID=$(head -n 1 "$PG_PID_FILE")
    echo "Stopping PostgreSQL service (PID: $PG_PID)..." | tee -a "$LOG_FILE"
    su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D /var/lib/postgresql/data stop"

    # 等待 PostgreSQL 停止
    sleep 5
    if [ -f "$PG_PID_FILE" ] || su - postgres -c "$PG_CTL_PATH -D $DATA_DIR status" | grep -q "server is running"; then
        echo "Failed to stop PostgreSQL service." | tee -a "$LOG_FILE"
        exit 1
    fi
else
    echo "PostgreSQL PID file not found." | tee -a "$LOG_FILE"
    exit 1
fi

# 备份数据目录
echo "Backing up data directory from $DATA_DIR to $BACKUP_DIR..." | tee -a "$LOG_FILE"
cp -r "$DATA_DIR" "$BACKUP_DIR"

# 检查备份是否成功
if [ $? -eq 0 ]; then
    echo "Backup completed successfully." | tee -a "$LOG_FILE"
else
    echo "Backup failed." | tee -a "$LOG_FILE"
    exit 1
fi

# 启动 PostgreSQL 服务
echo "Starting PostgreSQL service..." | tee -a "$LOG_FILE"
su - postgres -c "$PG_CTL_PATH -D $DATA_DIR start"

# 检查 PostgreSQL 服务是否已启动
if ! su - postgres -c "$PG_CTL_PATH -D $DATA_DIR status" | grep -q "server is running"; then
    echo "Failed to start PostgreSQL service." | tee -a "$LOG_FILE"
    exit 1
fi

echo "PostgreSQL service started successfully." | tee -a "$LOG_FILE"
