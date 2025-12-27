# 模块 Extra: Git 版本控制基础与进阶

Git 是程序员的时光机。它不仅能保存代码的历史版本，还能让你在犯错时“穿越”回去修复问题。

本章将介绍 Git 的基础操作，并重点讲解如何优雅地修正提交历史中的错误（比如提交了错误的作者信息）。

## 1. 基础配置与工作流

### 初次见面：自报家门
在使用 Git 之前，必须告诉它你是谁。这会作为签名出现在你的每一次提交中。

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 核心三部曲
Git 的日常工作流主要由三个命令组成：

1.  **`git add`**: 将文件放入“暂存区” (Staging Area)。
    *   `git add .` (添加所有修改)
    *   `git add filename.py` (添加指定文件)
2.  **`git commit`**: 将暂存区的内容永久保存到仓库历史中。
    *   `git commit -m "描述你做了什么"`
3.  **`git status`**: 查看当前状态（哪些文件改了没交，哪些文件已经暂存）。

## 2. 进阶技巧：后悔药与时光倒流

### 场景 A：刚提交完发现写错了/漏了文件
如果你刚刚执行了 `git commit`，但发现注释写错了，或者漏了一个文件没 add。

```bash
# 1. 如果有漏掉的文件，先 add 进去
git add forgotten_file.py

# 2. 使用 --amend 参数修改上一次提交
# 这会打开编辑器让你修改提交信息，并且把新 add 的文件合并到上一次提交中
git commit --amend
```

### 场景 B：提交了错误的作者信息 (修改历史)
这是一个非常经典的问题：你在公司电脑上用了私人邮箱提交，或者反过来。

#### 情况 1：只修改最近一次提交
```bash
git commit --amend --author="New Name <new.email@example.com>" --no-edit
```

#### 情况 2：修改过去所有的提交 (核弹级操作)
如果你发现整个项目的提交记录作者都错了（比如刚初始化项目时没配置好），可以使用 `git rebase` 来批量修改。

**警告**: 修改历史会改变 Commit ID。如果这些代码已经推送到多人协作的远程仓库，请谨慎操作！

```bash
# 1. 设置正确的本地配置
git config user.name "Correct Name"
git config user.email "correct@email.com"

# 2. 从根节点开始变基 (Rebase)，对每一个提交执行 amend 命令
git rebase --root --exec "git commit --amend --no-edit --reset-author"
```

这条命令的含义是：
*   `--root`: 从第一条 commit 开始处理。
*   `--exec`: 对每一条 commit 执行后面的命令。
*   `--reset-author`: 将作者信息重置为当前 `git config` 中配置的值。

## 3. 常用查看命令

*   `git log`: 查看详细历史。
*   `git log --oneline`: 查看简洁历史（一行一条）。
*   `git log --graph`: 查看分支合并图。

---

> 🤖 **AI 助手时间**:
>
> *   **Prompt**: "解释一下 `git merge` 和 `git rebase` 的区别，用图解的方式描述。"
> *   **Action**: 在 VS Code 中打开 Copilot Chat 提问。
> *   **Reflection**: 为什么很多开源项目维护者更喜欢 Rebase？它对提交历史的整洁度有什么影响？
