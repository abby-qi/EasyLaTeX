# Docker构建说明

## 构建镜像

### Linux/macOS
```bash
docker build -t easylatex -f docker/Dockerfile .
```

### Windows (PowerShell)
```powershell
docker build -t easylatex -f docker/Dockerfile .
```

## 运行容器

### 使用docker-compose（推荐）
```bash
docker-compose -f docker/docker-compose.yml up
```

### 使用docker run
```bash
docker run -it -p 3000:3000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/output:/app/output \
  easylatex
```

## 注意事项

1. **TinyTeX安装**: Dockerfile会自动下载和安装TinyTeX，首次构建可能需要较长时间
2. **端口映射**: 默认使用3000端口，可通过修改docker-compose.yml调整
3. **卷挂载**: config和output目录会挂载到容器，方便持久化配置和导出文件
4. **平台支持**: 当前Dockerfile主要针对Linux平台，Windows和macOS可能需要调整

## 故障排查

### 构建失败
- 检查网络连接（需要下载TinyTeX）
- 检查Docker磁盘空间
- 查看构建日志了解具体错误

### 运行失败
- 检查端口3000是否被占用
- 检查Python和Node.js版本兼容性
- 查看容器日志：`docker logs easylatex`