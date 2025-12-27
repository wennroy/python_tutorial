# 模块 Extra: Docker 环境搭建指南

在现代开发中，Docker 已经成为不可或缺的工具。它能确保你的代码在任何机器上都能以相同的环境运行，彻底解决 "在我机器上是好的" (It works on my machine) 这一经典问题。

本指南将教你如何在三大主流操作系统上安装 Docker。

## 1. Windows 安装 (推荐使用 WSL2)

Windows 用户推荐使用 **Docker Desktop** 配合 **WSL 2** (Windows Subsystem for Linux 2) 后端，性能最好且体验最接近原生 Linux。

### 前置要求
*   Windows 10 (版本 2004 及更高) 或 Windows 11。
*   已启用 WSL 2 功能。

### 安装步骤
1.  **下载**: 访问 [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) 下载安装包。
2.  **安装**: 双击运行安装程序。
    *   确保勾选 "Use WSL 2 instead of Hyper-V" (推荐)。
3.  **启动**: 安装完成后，启动 Docker Desktop。
4.  **配置 WSL 2 (如果尚未配置)**:
    *   Docker Desktop 可能会提示你更新 WSL 内核，按照提示链接下载安装即可。
    *   打开 PowerShell，运行 `wsl --set-default-version 2`。

## 2. macOS 安装

macOS 用户同样使用 **Docker Desktop**。

### 注意事项
*   请根据你的芯片类型 (Intel 或 Apple Silicon/M1/M2/M3) 下载对应的版本。

### 安装步骤
1.  **下载**: 访问 [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)。
    *   如果是 M1/M2/M3 芯片，选择 **Mac with Apple silicon**。
    *   如果是 Intel 芯片，选择 **Mac with Intel chip**。
2.  **安装**: 双击 `.dmg` 文件，将 Docker 图标拖入 Applications 文件夹。
3.  **启动**: 在“应用程序”中找到 Docker 并启动。顶部菜单栏会出现鲸鱼图标。

## 3. Ubuntu (Linux) 安装

Linux 环境通常使用服务器版本 (Docker Engine)，当然也可以安装 Docker Desktop for Linux，但这里介绍最通用的命令行安装方法。

### 安装步骤 (使用官方仓库)

打开终端，依次运行以下命令：

1.  **卸载旧版本 (如有)**:
    ```bash
    sudo apt-get remove docker docker-engine docker.io containerd runc
    ```

2.  **设置仓库**:
    ```bash
    # 更新 apt 包索引
    sudo apt-get update
    
    # 安装依赖包
    sudo apt-get install ca-certificates curl gnupg
    
    # 添加 Docker 官方 GPG 密钥
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    
    # 设置仓库
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

3.  **安装 Docker Engine**:
    ```bash
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

4.  **免 sudo 使用 Docker (可选)**:
    ```bash
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    ```

## 4. 验证安装

无论哪个系统，安装完成后打开终端 (Terminal/PowerShell)，运行以下命令验证：

```bash
# 查看版本
docker --version

# 运行 Hello World 容器
docker run hello-world
```

如果看到 "Hello from Docker!" 的欢迎信息，说明安装成功！

---

> 🤖 **AI 助手时间**:
>
> *   **Prompt**: "解释一下 Docker 中的 Image (镜像) 和 Container (容器) 有什么区别？用生活中的例子打比方。"
> *   **Action**: 在 VS Code 中打开 Copilot Chat 提问。
> *   **Reflection**: AI 的比喻（比如菜谱与菜肴、模具与饼干）是否让你更容易理解了？
