# coding=utf-8

from multiprocessing import Process, freeze_support

def process_data(filelist):
    for filepath in filelist:
        print('Processing {} ...'.format(filepath))
        # 处理数据
        # ...

if __name__ == '__main__':
    # 如果是在Windows下，还需要加上freeze_support()
    freeze_support()
    
    # full_list包含了要处理的全部文件列表
    full_list = [x for x in xrange(100)]

    n_total = len(full_list) # 一个远大于32的数
    n_processes = 32

    # 每段子列表的平均长度
    length = float(n_total) / float(n_processes)
    
    # 计算下标，尽可能均匀地划分输入文件列表
    indices = [int(round(i*length)) for i in range(n_processes+1)]
    
    # 生成每个进程要处理的子文件列表
    sublists = [full_list[indices[i]:indices[i+1]] for i in range(n_processes)]
    
    # 生成进程
    processes = [Process(target=process_data, args=(x,)) for x in sublists]

    # 并行处理
    for p in processes:
        p.start()

    for p in processes:
        p.join()