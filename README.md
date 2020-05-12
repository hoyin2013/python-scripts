# python-scripts

python写的一些运维小脚本

- osx在clone到本地以后，`git push`时报403错误，`vi .git/config`，将`url = https://github.com`修改成`url=https://用户名:密码@github.com`

- 几个git命令
  
```bash
# 配置
git config user.user ""
git config user.email ""
git config credential.helper store

# 取代码
git pull origin master

# 更新到git
git add *
git commit -m ""
git push origin master  

# 创建分支
git checkout -b branch_name

```

