## shutil

也是用来文件操作，但是它与os不同的是它只用来文件或文件夹操作

- shutil.copyfile('oldfile','newfile') 参数只能是文件，新文件不存在则创建
- shutil.copy("oldfile","newfileordir") olddir只能是文件，newfileordir可以是文件或文件夹
- shutil.copytree("olddir","newdir") 参数只能是目录，且newdir必须不存在
- shutil.move("oldpos","newpos") 移动文件或文件夹
- shutil.rmtree("dir") 可以空目录或者是有非空目录