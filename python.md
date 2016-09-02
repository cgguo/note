# log模块端独写
参考教程：http://www.jianshu.com/p/e3abceb9ab43
http://python.jobbole.com/82221/

### Python异常管理
- **捕获**: 如果不对抛出的异常进行捕获，那么python会打印堆栈信息推出,可以通过try...except...来处理异常.
- **抛出**: python内建异常触发后会自动抛出，也可以使用raise Exception主动抛出任何异常.
- **自定义**: 很多时候对会自定义异常供自己的程序使用，例如自定义一个启动失败异常。

### 内置异常

内置异常|    含义|
---|---
Exception |   所有异常的基类
AttributeError |  特性引用或复制失败
IOError | 试图打开不存在的文件
IndexError |  序列中不存在索引时发生
KeyError |   映射中不存在键值时发生
NameError |   找不到变量名字时发生
SyntaxError | 语法错误发生
TypeError |  内建操作或这函数应用于错误类型的对象时发生
ValueError | 内建操作或这函数应用于正确的对象,但是对象使用不合适的值
ZeroDivisionError |   除法或者模除第二个参数为0时候引发

### 捕获异常
在python中，通过try...except...来捕获是哪里出现异常
```python
try:
    #statement
    ...
except exception1:
    #handle type of exception1
    ...
except exception2:
    #handle type of exception2
    ...
except:
    #handle any type of exception
    ...
else:
    #when no exception occures, excute here
    ...
finally:
    #whether exception occures or not, it will excute here
    ...
```

如果在执行statement代码的过程中，接收到了异常，此时会终止statement的继续执行，跳转到异常的捕获处理情况，依次判断每一个except分支，直到有符合的except object，则会执行对应的异常处理分支，如果都没有符合的分支，则会跳转到执行finally去执行，并且将此异常继续传递给调用者。如果statement代码没有发生异常，则会执行else分支的代码，最后执行finally中的代码。

如果异常没有被捕获处理，则会一直向上层传播，直至有代码对其捕获处理。如果直到最上层都没有捕获处理，解释器就会退出终止程序，同时打印Traceback信息，以便让用户找到错误产生的原因。

**执行流程总结：finally始终都执行，无异常还执行else**
`try->异常->except->finally`
`try->无异常->else->finally`


### 抛出或触发异常Raise
在Python中，通过raise来向上抛出一个exception，可以判断程序是什么错误类型

```python
#coding=utf-8
def functionName( level ):
    if level < 1:
        raise Exception("Invalid level!", level)
        # 触发异常后，后面的代码就不会再执行

functionName(0)
```

注意：虽然大多数错误会导致异常，但一个异常不一定代表错误，有时候它们只是一个警告，有时候它们可能是一个终止信号，比如退出循环等。


## 跟踪和查看异常
发生异常时，Python能“记住”引发的异常以及程序的当前状态，Python还维护着traceback（跟踪）对象，其中含有异常发生时与函数调用堆栈有关的信息，异常可能在一系列嵌套较深的函数调用中引发，程序调用每个函数时，Python会在“函数调用堆栈”的起始处插入函数名，一旦异常被引发，Python会搜索一个相应的异常处理程序。

如果当前函数中没有异常处理程序，当前函数会终止执行，Python会搜索当前函数的调用函数，并以此类推，直到发现匹配的异常处理程序，或者Python抵达主程序为止，这一查找合适的异常处理程序的过程就称为“堆栈辗转开解”（Stack Unwinding）。解释器一方面维护着与放置堆栈中的函数有关的信息，另一方面也维护着与已从堆栈中“辗转开解”的函数有关的信息。

`traceback.print_exc()`：打印异常

### 打印输出不是个好办法
尽管记录日志非常重要，但是并不是所有的开发者都能正确地使用它。我曾看到一些开发者是这样记录日志的，在开发的过程中插入 print 语句，开发结束后再将这些语句移除。就像这样:
```python
print 'Start reading database'
records = model.read_recrods()
print '# records', records
print 'Updating record ...'

model.update_records(records)
print 'done'

```
如果是简单的脚本可以这么写，对于复杂软件做好信息分类很重要，更方便快捷的查找你想要的信息。

### 使用Python的标准日志模块
Python标准日志模块非常简单易用，十分灵活
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Start reading database')
# read database here

records = {'john': 55, 'tom': 66}
logger.debug('Records: %s', records)
logger.info('Updating records ...')
# update records here

logger.info('Finish updating records')

# result
INFO:__main__:Start reading database
INFO:__main__:Updating records ...
INFO:__main__:Finish updating records
```
你可能会问这与使用 `print` 有什么不同呢。它有以下的优势：

- 你可以控制消息的级别，过滤掉那些并不重要的消息。
- 你可决定输出到什么地方，以及怎么输出。

### logging 常用功能介绍
#### Formatter

参数 |  含义
------------ | -----
%(name)s |    Logger的名字
%(levelno)s | 数字形式的日志级别
%(levelname)s |   文本形式的日志级别
%(pathname)s |    调用日志输出函数的模块的完整路径名，可能没有
%(filename)s |    调用日志输出函数的模块的文件名
%(module)s |  调用日志输出函数的模块名
%(funcName)s |    调用日志输出函数的函数名
%(lineno)d |  调用日志输出函数的语句所在的代码行
%(created)f | 当前时间，用UNIX标准的表示时间的浮点数表示
%(relativeCreated)d | 输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s | 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d |  线程ID。可能没有
%(threadName)s |  线程名。可能没有
%(process)d | 进程ID。可能没有
%(message)s | 用户输出的消息

#### SetLevel
有许多的重要性别级可供选择`level`，`debug`、`info`、`warning`、`error` 以及 `critical`。

#### Handler
- **logging.StreamHandler**：使用这个Handler可以向类似与`sys.stdout`或者`sys.stderr`的任何文件对象`(file object)`输出信息。
它的构造函数是：`StreamHandler([strm])`，其中strm参数是一个文件对象，默认是`sys.stderr`

- **logging.FileHandler**：和`StreamHandler`类似，用于向一个文件输出日志信息。不过FileHandler会帮你打开这个文件。它的构造函数是：`FileHandler(filename[,mode])`,`filename`是文件名，必须指定一个文件名。`mode`是文件的打开方式,默认是`"a"`，即添加到文件末尾。

- **logging.handlers.RotatingFileHandler**:这个Handler类似于上面的`FileHandler`，但是它可以管理文件大小。当文件达到一定大小之后，它会自动将当前日志文件改名，然后创建一个新的同名日志文件继续输出。比如日志文件是`chat.log`。当chat.log达到指定的大小之后，`RotatingFileHandler`自动把 文件改名为`chat.log.1`。不过，如果`chat.log.1`已经存在，会先把chat.log.1重命名为`chat.log.2`。。。最后重新创建 `chat.log`，继续输出日志信息。它的构造函数是：`RotatingFileHandler( filename[, mode[, maxBytes[, backupCount]]])`
其中`filename`和`mode`两个参数和`FileHandler`一样。`maxBytes`用于指定日志文件的最大文件大小。如果`maxBytes`为0，意味着日志文件可以无限大，这时上面描述的重命名过程就不会发生。
`backupCount`用于指定保留的备份文件的个数。比如，如果指定为`2`，当上面描述的重命名过程发生时，原有的`chat.log.2`并不会被更名，而是被删除。

- 其他Handler可查帮助
    logging.handlers.TimedRotatingFileHandler
    logging.handlers.SocketHandler
    logging.handlers.DatagramHandler
    logging.handlers.SysLogHandler
    logging.handlers.NTEventLogHandler
    logging.handlers.SMTPHandler
    logging.handlers.MemoryHandler
    logging.handlers.HTTPHandler

**FileHandler实例**
通过`handler` 把不同的级别，你就可以只输出错误消息到特定的记录文件中，或者在调试时只记录调试信息。让我们把 `logger` 的级别改成 `DEBUG` 再看一下输出结果：

```python
# 修改上面的代码
logging.basicConfig(level=logging.DEBUG)

# result
INFO:__main__:Start reading database
DEBUG:__main__:Records: {'john': 55, 'tom': 66}
INFO:__main__:Updating records ...
INFO:__main__:Finish updating records
```

正如看到的那样，我们把 `logger` 的等级改为 `DEBUG`后，调试记录就出现在了输出当中。你也可以选择怎么处理这些消息。例如，你可以使用 `FileHandler` 把记录写进文件中：

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('hello.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.info('Hello baby')
```

标准库模块中提供了许多的 handler ，你可以将记录发送到邮箱甚至发送到一个远程的服务器。你也可以实现自己的记录 handler 。这里将不具体讲述实现的细节，你可以参考官方文档:
[Basci Turial](https://docs.python.org/2/howto/logging.html#logging-basic-tutorial)
[Advanced Tutorial](https://docs.python.org/2/howto/logging.html#logging-advanced-tutorial)
[Logging Cookbook](https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook)


### 以合适的等级输出日志记录
- Debug：大多数的情况下，你都不想阅读日志中的太多细节。因此，只有你在调试过程中才会使用 DEBUG 等级。我只使用 DEBUG 获取详细的调试信息，特别是当数据量很大或者频率很高的时候，比如算法内部每个循环的中间状态。
```python
def complex_algorithm(items):
    for i, item in enumerate(items):
        # do some complex algorithm computation

        logger.debug('%s iteration, item=%s', i, item)
```

- Info：在处理请求或者服务器状态变化等日常事务中，我会使用 INFO 等级。

```python
def handle_request(request):
    logger.info('Handling request %s', request)
    # handle request here

    result = 'result'
    logger.info('Return result: %s', result)

def start_service():
    logger.info('Starting service at port %s ...', port)
    service.start()
    logger.info('Service is started')
```

- Warning：当发生很重要的事件，但是并不是错误时，我会使用 WARNING 。比如，当用户登录密码错误时，或者连接变慢时。
```python
def authenticate(user_name, password, ip_address):
    if user_name != USER_NAME and password != PASSWORD:
        logger.warn('Login attempt to %s from IP %s', user_name, ip_address)
        return False
    # do authentication here
```

- Error: 有错误发生时肯定会使用 ERROR 等级了。比如抛出异常，IO 操作失败或者连接问题等。
```python
def get_user_by_id(user_id):
    user = db.read_user(user_id)
    if user is None:
        logger.error('Cannot find user with user_id=%s', user_id)
        return user
    return user
```

- Critical:我很少使用 CRITICAL, 当一些特别糟糕的事情发生时，你可以使用这个级别来记录。比方说，内存耗尽，磁盘满了或者核危机。

**使用`__name__`作为`logger`的名称**
虽然不是非得将 logger 的名称设置为 __name__ ，但是这样做会给我们带来诸多益处。在 python 中，变量 __name__ 的名称就是当前模块的名称。比如，在模块 “foo.bar.my_module” 中调用 logger.getLogger(__name__) 等价于调用logger.getLogger(“foo.bar.my_module”) 。当你需要配置 logger 时，你可以配置到 “foo” 中，这样包 foo 中的所有模块都会使用相同的配置。当你在读日志文件的时候，你就能够明白消息到底来自于哪一个模块。

**捕捉异常并使用 `traceback` 记录它**
出问题的时候记录下来是个好习惯，但是如果没有 traceback ，那么它一点儿用也没有。你应该捕获异常并用 traceback 把它们记录下来。比如下面这个例子：
```python
try:
    open('/path/to/does/not/exist', 'rb')
except (SystemExit, KeyboardInterrupt):
    raise
except Exception, e:
    logger.error('Failed to open file', exc_info=True)
```

使用参数 `exc_info=true` 调用 `logger` 方法, `traceback` 会输出到 `logger` 中。你可以看到下面的结果：

```python
# result
ERROR:__main__:Failed to open file
Traceback (most recent call last):
  File "example.py", line 6, in <module>
    open('/path/to/does/not/exist', 'rb')
IOError: [Errno 2] No such file or directory: '/path/to/does/not/exist'
```

你也可以调用 `logger.exception(msg, _args)`，它等价于 `logger.error(msg, exc_info=True, _args)`。


**多模块同时使用logging**

logging模块保证在同一个python解释器内，多次调用logging.getLogger('log_name')都会返回同一个logger实例，即使是在多个模块的情况下。所以典型的多模块场景下使用logging的方式是在main模块中配置logging，这个配置会作用于多个的子模块，然后在其他模块中直接通过getLogger获取Logger对象即可。

`python2.7` 之后的版本中 `fileConfg` 与 `dictConfig` 都新添加了 `disable_existing_loggers` 参数，将其设置为 `False`，会已经存在的logger正常创建，默认是True。例如：

```python
import logging
import logging.config

logger = logging.getLogger(__name__)

# load config from file

# logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

# or, for dictConfig

logging.config.dictConfig({
    'version': 1,              
    'disable_existing_loggers': False,  # this fixes the problem

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',    
            'class':'logging.StreamHandler',
        },  
    },
    'loggers': {
        '': {                  
            'handlers': ['default'],        
            'level': 'INFO',  
            'propagate': True  
        }
    }
})

logger.info('It works!')
```

### 使用 JSON 或者 YAML 记录配置
虽然你可以在 python 代码中配置你的日志系统，但是这样并不够灵活。最好的方法是使用一个配置文件来配置。在 Python2.7 及之后的版本中，你可以从字典中加载 logging 配置。这也就意味着你可以从 JSON 或者 YAML 文件中加载日志的配置。尽管你还能用原来 .ini 文件来配置，但是它既很难读也很难写。下面我给你们看一个用 JSON 和 YAML 文件配置的例子:

从logging.json的文件类型读入日志的配置信息：
```python
import json
import logging.config

def setup_logging(default_path='logging.json',
                default_level=logging.INFO,
                env_key='LOG_CFG'):

    #Setup logging configuration
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
```

使用 JSON 的一个优点就是 json是一个标准库，你不需要额外安装它。但是从我个人来说，我比较喜欢 YAML 一些。它无论是读起来还是写起来都比较容易。你也可以使用下面的方法来加载一个 YAML 配置文件：

```python
import os
import logging.config

import yaml

def setup_logging(default_path='logging.yaml',
                default_level=logging.INFO,
                env_key='LOG_CFG'):
    #Setup logging configuration
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
```

**使用旋转文件句柄RotatingFileHandler**
如果你用 FileHandler 写日志，文件的大小会随着时间推移而不断增大。最终有一天它会占满你所有的磁盘空间。为了避免这种情况出现，你可以在你的生成环境中使用 RotatingFileHandler 替代 FileHandler。

### 总结
Python 的日志库设计得如此之好，真是让人欣慰，我觉得这是标准库中最好的一部分了，你不得不选择它。它很灵活，你可以用你自己的 handler 或者 filter。已经有很多的第三方的 handler 了，比如 pyzmq 提供的 ZeroMQ 日志句柄，它允许你通过 zmq 套接字发送日志消息。如果你还不知道怎么正确的使用日志系统，这篇文章将会非常有用。有了很好的日志记录实践，你就能非常容易地发现系统中的问题。这是很非常值得投资的。

[原文](http://python.jobbole.com/81666/)
